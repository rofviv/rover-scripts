from rplidar import RPLidar
import os
import time
import subprocess
import threading
from flask import Flask, jsonify, render_template
from threading import Thread

# Configuraciones iniciales
project_root = os.getenv('PROJECT_ROOT', '')
ip_remote_mavproxy = os.getenv('IP_REMOTE_MAVPROXY', '192.168.18.20')
port = ":14550"
port_com_lidar = os.getenv('PORT_COM_LIDAR', 'COM10')
lidar = RPLidar(port_com_lidar, 256000)
session_name = os.getenv('SESSION_NAME', "mavproxy_session")

range_distance = 2000
range_distance_max = 4000
range_angle = 30
half_range_angle = range_angle / 2
min_angle = 0.0
max_angle = 359.9

object_detected = False
sensor_mode = 1

# Datos del LiDAR para mostrar en el navegador
lidar_data = []

# Crear la aplicación Flask
app = Flask(__name__)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para obtener los datos del LiDAR
@app.route('/lidar-data')
def get_lidar_data():
    print(lidar_data)
    return jsonify(lidar_data)

# Ruta para obtener el estado de las variables
@app.route('/variables')
def get_variables():
    variables = {
        'sensor_mode': sensor_mode,
        'object_detected': object_detected,
        'range_distance': range_distance
    }
    return jsonify(variables)

# Iniciar el servidor Flask en un hilo separado
def start_flask_server():
    app.run(host='0.0.0.0', port=5000)

# Leer el modo de los sensores desde un archivo
def read_sensor_mode():
    global sensor_mode
    try:
        with open(f"{project_root}\\mode_sensores.txt", "r") as file:
            mode = file.read().strip()
            sensor_mode = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo mode_sensores.txt: {e}")

# Enviar comandos a WSL
def send_command_to_wsl(command):
    return
    wsl_command = f'screen -S {session_name} -p 0 -X stuff "{command}\\n"'
    subprocess.run(f'wsl {wsl_command}', shell=True)

# Ejecutar comandos en segundo plano
def execute_commands():
    commands = [
        'output remove 1',
        'rc 6 1000',
        'rc 2 2000',
        'rc 6 0',
        'rc 2 0',
    ]
    for command in commands:
        send_command_to_wsl(command)

# Ejecutar los comandos en un hilo separado
def execute_commands_in_thread():
    command_thread = threading.Thread(target=execute_commands)
    command_thread.start()

# Monitorizar cambios en el modo de sensores
def monitor_mode_changes():
    global sensor_mode
    while True:
        read_sensor_mode()
        time.sleep(5)

# Función principal del script
def main():
    global object_detected, lidar_data

    # Iniciar el servidor Flask en un hilo
    flask_thread = Thread(target=start_flask_server)
    flask_thread.daemon = True
    flask_thread.start()

    # Iniciar el monitoreo de cambios en el modo de sensores
    mode_thread = threading.Thread(target=monitor_mode_changes)
    mode_thread.daemon = True
    mode_thread.start()

    print("Starting spinning .......\n")
    time.sleep(5)
    print("Scanning started\n")
    print(f"Range distance = {range_distance}")

    try:
        for scan in lidar.iter_scans():
            lidar_data.clear()  # Limpiar los datos anteriores del LiDAR
            object_still_detected = False
            
            for (_, angle, distance) in scan:
                if (distance < range_distance_max):
                    lidar_data.append({'angle': angle, 'distance': distance})  # Añadir datos del LiDAR
                if (angle >= (max_angle - half_range_angle) or angle <= (min_angle + half_range_angle)) and distance < range_distance:
                    object_still_detected = True
                    if sensor_mode == 1:
                        if not object_detected:
                            print(f"Objeto detectado a {distance} mm en el ángulo {angle} grados")
                            print("Ejecutando comandos en segundo plano...\n")
                            execute_commands_in_thread()
                        object_detected = True
                    break
                #elif distance < range_distance_max:
                 #   lidar_data.append({'angle': angle, 'distance': distance})  # Añadir datos del LiDAR
            
            if not object_still_detected and object_detected:
                if sensor_mode == 1:
                    print("Objeto desaparecido, ejecutando el último comando...\n")
                    send_command_to_wsl(f'output add {ip_remote_mavproxy}{port}')
                object_detected = False 

            if sensor_mode == 0:
                if object_detected:
                    print("Modo sensores desactivado, ejecutando el último comando...\n")
                    send_command_to_wsl(f'output add {ip_remote_mavproxy}{port}')
                    object_detected = False

    except KeyboardInterrupt:
        print('Stopping.')

    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == "__main__":
    main()
