from rplidar import RPLidar
import os
import time
import subprocess
import threading

project_root = os.getenv('PROJECT_ROOT', '')
ip_remote_mavproxy = os.getenv('IP_REMOTE_MAVPROXY', '192.168.18.20')
port = ":14550"
port_com_lidar = os.getenv('PORT_COM_LIDAR', 'COM10')
lidar = RPLidar(port_com_lidar, 256000)
session_name = os.getenv('SESSION_NAME', "mavproxy_session")

range_distance = 2500
range_angle = 30
half_range_angle = range_angle / 2
min_angle = 0.0
max_angle = 359.9

object_detected = False
sensor_mode = 1

def read_sensor_mode():
    global sensor_mode
    try:
        with open(f"{project_root}\mode_sensores.txt", "r") as file:
            mode = file.read().strip()
            sensor_mode = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo mode_sensores.txt: {e}")

def send_command_to_wsl(command):
    wsl_command = f'screen -S {session_name} -p 0 -X stuff "{command}\\n"'
    subprocess.run(f'wsl {wsl_command}', shell=True)

def execute_commands():
    print("Send command")
    commands = [
        'output remove 1',
        'rc 6 1000',
        'rc 2 2000',
        'rc 6 0',
        'rc 2 0',
        # 'mode hold'
    ]
    
    for command in commands:
        send_command_to_wsl(command)

def execute_commands_in_thread():
    command_thread = threading.Thread(target=execute_commands)
    command_thread.start()

def monitor_mode_changes():
    global sensor_mode
    while True:
        read_sensor_mode()
        time.sleep(5)

def main():
    global object_detected

    mode_thread = threading.Thread(target=monitor_mode_changes)
    mode_thread.daemon = True
    mode_thread.start()

    print("Starting spinning .......\n")
    time.sleep(5)
    print("Scanning started\n")
    print(f"Range distance = {range_distance}")

    try:
        for scan in lidar.iter_scans():
            object_still_detected = False
            
            for (_, angle, distance) in scan:
                if (angle >= (max_angle - half_range_angle) or angle <= (min_angle + half_range_angle)) and distance < range_distance:
                    object_still_detected = True
                    if sensor_mode == 1:
                        if not object_detected:
                            print(f"Objeto detectado a {distance} mm en el ángulo {angle} grados")
                            print("Ejecutando comandos en segundo plano...\n")
                            execute_commands_in_thread()
                        object_detected = True
                    break
            
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
