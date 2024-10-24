import serial
import time
import subprocess
import threading
import os

# Configuración del puerto serie y la sesión de MAVProxy
session_name = os.getenv('SESSION_NAME', "mavproxy_session")
arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)
ip_remote_mavproxy = os.getenv('IP_REMOTE_MAVPROXY', '192.168.18.20')
port = ":14550"

# Inicializamos el estado de los sensores (False significa que no están detectando objetos)
estado_sensores = {1: False, 2: False}
# Control de tiempo desde la última detección por sensor
ultimo_tiempo_deteccion = {1: time.time(), 2: time.time()}

# Bandera para saber si el comando neutral ya ha sido enviado
neutral_command_sent = False
# Bandera para saber si el comando stop ya ha sido enviado
stop_command_sent = False

# Definir un tiempo de espera máximo (en segundos)
TIEMPO_MAX_ESPERA = 0.5  # 1 segundo sin datos significa que el objeto ya no está
MAX_DISTANCE = 20

# Función para enviar comandos a WSL con MAVProxy
def send_command_to_wsl(command):
    wsl_command = f'screen -S {session_name} -p 0 -X stuff "{command}\\n"'
    try:
        subprocess.run(f'wsl {wsl_command}', shell=True)
    except Exception as e:
        print(f"Error al enviar comando a WSL: {e}")

# Función para ejecutar comandos en MAVProxy
def execute_command(commands):
    #print(commands)
    send_command_to_wsl('output remove 1')
    # send_command_to_wsl(command)
    for command in commands:
        send_command_to_wsl(command)
    send_command_to_wsl(f'output add {ip_remote_mavproxy}{port}')

# Funciones que definen los comandos de izquierda y derecha
def get_left_commands():
    return ['rc 1 2000', 'rc 1 0']

def get_right_commands():
    return ['rc 1 1000', 'rc 1 0']

def get_center_commands():
    return ['rc 1 1500', 'rc 1 0']

def get_neutral_commands():
    return ['rc 7 1500', 'rc 7 0']

def get_stop_commands():
    return ['output list']
    # return 'rc 3 1000'

# Función para manejar la lógica de los sensores
def manejar_sensor(sensor, distancia):
    global estado_sensores, ultimo_tiempo_deteccion, neutral_command_sent, stop_command_sent

    # Verificamos si detecta un objeto
    if distancia < MAX_DISTANCE:
        ultimo_tiempo_deteccion[sensor] = time.time()
        if not estado_sensores[sensor]:  # Si antes no estaba detectando
            estado_sensores[sensor] = True  # Actualizamos el estado a "detectando"
            if sensor == 1:
                command = get_right_commands()  # Comando al detectar con sensor 1
            elif sensor == 2:
                command = get_left_commands()  # Comando al detectar con sensor 2
            execute_command(command)  # Ejecutamos el comando
            neutral_command_sent = False  # Resetear la bandera cuando se detecta algo
            print(f"Sensor {sensor} detecta objeto a {distancia} cm. Ejecutado: {command}")

# Función para verificar si algún sensor ha dejado de detectar (por timeout)
def verificar_sensores_timeout():
    global estado_sensores, ultimo_tiempo_deteccion, neutral_command_sent, stop_command_sent

    tiempo_actual = time.time()

    # Verifica si algún sensor sigue detectando
    check_object = any(estado_sensores[sensor] for sensor in estado_sensores.keys())
    
    for sensor in estado_sensores.keys():
        # Si ha pasado más de TIEMPO_MAX_ESPERA sin recibir datos del sensor
        if estado_sensores[sensor] and (tiempo_actual - ultimo_tiempo_deteccion[sensor]) > TIEMPO_MAX_ESPERA:
            # Si el sensor estaba detectando y ahora ya no, actualizamos su estado
            estado_sensores[sensor] = False  # Actualizamos el estado a "no detectando"
            estado_sensores[1] = False
            estado_sensores[2] = False
            print(f"Sensor {sensor} ya no detecta objeto (timeout).")

    # Si ambos sensores están detectando, ejecuta el comando de "parar"
    if estado_sensores[1] and estado_sensores[2] and not stop_command_sent:
        execute_command(get_stop_commands())  # Llama a la función correctamente
        stop_command_sent = True  # Marca que el comando stop fue enviado

    if stop_command_sent and (estado_sensores[1] != estado_sensores[2]):
        execute_command(get_neutral_commands())  # Enviar comando neutral primero
        stop_command_sent = False
        print("Comando neutral enviado.")

    # Si todos los sensores han dejado de detectar y no se ha enviado el comando neutral aún
    if not check_object and not neutral_command_sent:
        if stop_command_sent:
            execute_command(get_neutral_commands())  # Llama a la función correctamente
            print("Comando neutral enviado.")
        execute_command(get_center_commands())
        neutral_command_sent = True  # Marcar que el comando neutral ya fue enviado
        stop_command_sent = False  # Reinicia la bandera stop después de enviar el neutral
        print("Comando center enviado.")

# Función para leer los datos del sensor
def leer_sensor():
    try:
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8').strip()
                try:
                    # Procesamos los datos del sensor
                    datos = linea.split(',')
                    sensor = int(datos[0])
                    distancia = float(datos[1])

                    print(linea)
                    
                    # Llamamos a la lógica para manejar el estado del sensor
                    manejar_sensor(sensor, distancia)
                except (IndexError, ValueError):
                    print("Error al procesar los datos del sensor")
            # Verificamos si algún sensor dejó de detectar por timeout
            verificar_sensores_timeout()
            time.sleep(0.1)  # Ciclo continuo con un pequeño delay de 100ms para detectar cambios
    except Exception as e:
        print(f"Error en la lectura del sensor: {e}")
    finally:
        arduino.close()

# Ejecución principal
try:
    leer_sensor()
except KeyboardInterrupt:
    print("Programa detenido por el usuario")
finally:
    if arduino.is_open:
        arduino.close()
