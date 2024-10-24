from rplidar import RPLidar
import os
import time
import subprocess
import threading
import queue

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
commands_in_progress = False  # Controla si los comandos están en proceso
output_in_progress = False  # Controla si ya se envió un 'output remove'
command_queue = queue.Queue()

def read_sensor_mode():
    global sensor_mode
    try:
        with open(f"{project_root}\\mode_sensores.txt", "r") as file:
            mode = file.read().strip()
            sensor_mode = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo mode_sensores.txt: {e}")

def send_command_to_wsl(command):
    wsl_command = f'screen -S {session_name} -p 0 -X stuff "{command}\\n"'
    subprocess.run(f'wsl {wsl_command}', shell=True)

def command_executor():
    """Hilo que ejecuta comandos en segundo plano."""
    global commands_in_progress, output_in_progress
    while True:
        command = command_queue.get()  # Espera hasta que haya un comando en la cola
        if command is None:
            break  # Salir del hilo si se recibe un "None"
        print(f"Ejecutando comando: {command}")
        send_command_to_wsl(command)
        if "output add" in command:
            commands_in_progress = False  # Finaliza el ciclo de comandos
            output_in_progress = False  # Resetea la bandera de output

def add_commands_to_queue():
    """Añadir comandos a la cola si no hay comandos en progreso."""
    global commands_in_progress, output_in_progress
    if not commands_in_progress and not output_in_progress:
        # Solo añadir comandos si no hay otro conjunto de comandos en proceso
        commands = [
            'output remove 1',
            'rc 6 1000',
            'rc 2 2000',
            'rc 6 0',
            'rc 2 0',
            # 'mode hold'
        ]
        for command in commands:
            command_queue.put(command)  # Añade el comando a la cola
        commands_in_progress = True  # Activa la bandera cuando se añaden los comandos
        output_in_progress = True  # Indica que se ha enviado un 'output remove'

def monitor_mode_changes():
    global sensor_mode
    while True:
        read_sensor_mode()
        time.sleep(5)

def main():
    global object_detected, output_in_progress

    # Inicia el hilo que ejecutará comandos
    command_thread = threading.Thread(target=command_executor)
    command_thread.daemon = True
    command_thread.start()

    # Inicia el hilo que monitorea el cambio de modo
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
                        if not object_detected and not output_in_progress:
                            # Si un objeto es detectado y no se ha enviado un output remove
                            print(f"Objeto detectado a {distance} mm en el ángulo {angle} grados")
                            print("Añadiendo comandos a la cola...\n")
                            add_commands_to_queue()
                        object_detected = True
                    break
            
            if not object_still_detected and object_detected:
                if sensor_mode == 1 and output_in_progress:
                    # Si el objeto desaparece, solo envía el 'output add' si hubo un 'output remove'
                    print("Objeto desaparecido, añadiendo el último comando...\n")
                    command_queue.put(f'output add {ip_remote_mavproxy}{port}')
                object_detected = False 

            if sensor_mode == 0:
                if object_detected and output_in_progress:
                    # Si el sensor está apagado, enviar el último comando de salida
                    print("Modo sensores desactivado, añadiendo el último comando...\n")
                    command_queue.put(f'output add {ip_remote_mavproxy}{port}')
                    object_detected = False

    except KeyboardInterrupt:
        print('Stopping.')

    finally:
        # Añadir un "None" a la cola para detener el hilo de comandos
        command_queue.put(None)
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == "__main__":
    main()
