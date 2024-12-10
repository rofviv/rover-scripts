import socket
import os
import time
import serial
import threading
from datetime import datetime


project_root = os.getenv('PROJECT_ROOT', '')
arduino = serial.Serial(port='COM10', baudrate=9600, timeout=1)
arduino.reset_input_buffer()

MAX_DISTANCE = 20
MAX_DISTANCE_BACK = 80
sensor_mode = 1
sensor_back = 0


def read_sensor_mode():
    global sensor_mode
    try:
        with open(f"{project_root}\mode_sonar.txt", "r") as file:
            mode = file.read().strip()
            sensor_mode = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo mode_sonar.txt: {e}")


def read_back():
    global sensor_back
    try:
        with open(f"{project_root}\mode_back.txt", "r") as file:
            mode = file.read().strip()
            sensor_back = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo mode_back.txt: {e}")


def monitor_mode_changes():
    global sensor_mode
    while True:
        read_sensor_mode()
        read_back()
        time.sleep(5)


def manejar_sensor(sensor, distancia, max_distance):
    if distancia < max_distance:
        notificar_maestro(f"sonar-{sensor}")
        print(f"Sensor sonar-{sensor} detecta objeto a {distancia} cm")


def leer_sensor():
    mode_thread = threading.Thread(target=monitor_mode_changes)
    mode_thread.daemon = True
    mode_thread.start()

    try:
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8').strip()
                try:
                    if sensor_mode == 1:
                        datos = linea.split(',')
                        sensor = int(datos[0])
                        distancia = float(datos[1])

                        current_time = datetime.now().strftime('%H:%M:%S')
                        print(f"{current_time} - {linea}")

                        # manejar_sensor(sensor, distancia, MAX_DISTANCE)
                        if sensor_back == 1:
                            if sensor == 4:
                                manejar_sensor(sensor, distancia, MAX_DISTANCE_BACK)
                        elif sensor != 4:
                            manejar_sensor(sensor, distancia, MAX_DISTANCE)
                except (IndexError, ValueError):
                    print("Error al procesar los datos del sensor")

            time.sleep(0.1)
    except Exception as e:
        print(f"Error en la lectura del sensor: {e}")
    finally:
        arduino.close()


def notificar_maestro(mensaje):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 65432))
            s.sendall(mensaje.encode('utf-8'))
            print(f'Notificación "{mensaje}" enviada al maestro.')
    except ConnectionRefusedError:
        print('No se pudo conectar con el maestro. Reintentando...')


if __name__ == "__main__":
    try:
        leer_sensor()
    except KeyboardInterrupt:
        print("Programa detenido por el usuario")
    finally:
        if arduino.is_open:
            arduino.close()

