from rplidar import RPLidar
import os
import time
import socket
import threading

print("SCRIPT LIDAR")

project_root = os.getenv('PROJECT_ROOT', '')
port_com_lidar = "COM5"
lidar = RPLidar(port_com_lidar, 256000)

MAX_DISTANCE = 500
range_angle = 30
half_range_angle = range_angle / 2
min_angle = 0.0
max_angle = 359.9

sensor_mode = 1

def read_sensor_mode():
    global sensor_mode
    try:
        with open(f"{project_root}\mode_sensores.txt", "r") as file:
            mode = file.read().strip()
            sensor_mode = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo mode_sensores.txt: {e}")


def monitor_mode_changes():
    global sensor_mode
    while True:
        read_sensor_mode()
        time.sleep(5)


def notificar_maestro(mensaje):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 65432))
            s.sendall(mensaje.encode('utf-8'))  # Enviar el mensaje como bytes
            print(f'Notificación "{mensaje}" enviada al maestro.')
    except ConnectionRefusedError:
        print('No se pudo conectar con el maestro. Reintentando...')


def main():

    mode_thread = threading.Thread(target=monitor_mode_changes)
    mode_thread.daemon = True
    mode_thread.start()

    print("Starting spinning .......\n")
    time.sleep(5)
    print("Scanning started\n")
    print(f"Range distance = {MAX_DISTANCE}")

    try:
        for scan in lidar.iter_scans():
            
            for (_, angle, distance) in scan:
                if (angle >= (max_angle - half_range_angle) or angle <= (min_angle + half_range_angle)) and distance < MAX_DISTANCE:
                    if sensor_mode == 1:
                        print(f"Objeto detectado a {distance} mm en el ángulo {angle} grados")
                        print("Ejecutando comandos en segundo plano...\n")
                        notificar_maestro("lidar")
                    break
                
            time.sleep(0.1)

    except KeyboardInterrupt:
        print('Stopping.')

    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == "__main__":
    main()
