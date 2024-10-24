import os
import subprocess
import time
from pymavlink import mavutil

ip_local_mavproxy = os.getenv('IP_LOCAL_MAVPROXY', '0.0.0.0')
# Conexión a MAVLink (actualiza la dirección y el puerto según sea necesario)
connection_string = f"udp:{ip_local_mavproxy}:14551"  # Cambia esto a la dirección de tu Cube
master = mavutil.mavlink_connection(connection_string)

# Función para verificar el ping
def check_ping(host):
    try:
        # Ejecutar el comando ping y capturar la salida
        output = subprocess.check_output(["ping", "-n", "4", host])
        # Extraer el tiempo de respuesta en milisegundos
        lines = output.decode().strip().split("\n")
        for line in lines:
            if "time=" in line:
                # Extraer el tiempo y convertirlo a float
                time_ms = line.split("time=")[-1].split(" ")[0]
                time_ms = float(time_ms.replace('ms', ''))  # Eliminar 'ms' antes de convertir
                return time_ms
    except subprocess.CalledProcessError:
        print("Error al ejecutar el comando ping.")
    except ValueError:
        print("Error al convertir el tiempo a float.")
    return None

# Función para obtener el modo actual del vehículo
def get_current_mode():
    master.wait_heartbeat()
    mode = master.recv_match(type='HEARTBEAT', blocking=True)
    return mode.custom_mode  # Devuelve el modo actual como un entero

# Función para cambiar el modo del vehículo
def set_mode(mode):
    # Esperar hasta que el sistema esté listo
    master.wait_heartbeat()
    print("Conectado al vehículo.")

    # Obtener el ID del sistema y del componente
    system_id = master.target_system
    component_id = master.target_component
    
    # Obtener el modo en formato de texto
    mode_mapping = {
        'HOLD': 4,  # ID del modo HOLD (ajustar según sea necesario)
    }
    
    if mode in mode_mapping:
        mode_id = mode_mapping[mode]
        # Enviar el comando para cambiar el modo
        print(f"Cambiando a modo {mode}...")
        master.mav.set_mode_send(
            system_id,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id
        )
        print(f"Modo cambiado a {mode}.")
    else:
        print("Modo no reconocido.")

# Host a verificar
host_to_ping = os.getenv('IP_REMOTE_MAVPROXY', '192.168.18.20')
# host_to_ping = "8.8.8.8"  # Puedes cambiarlo a la dirección que desees
# host_to_ping="10.13.13.2" 

while True:
    ping_time = check_ping(host_to_ping)
    
    if ping_time is not None:
        print(f"Ping a {host_to_ping}: {ping_time} ms")
        
        # Verificar si el ping excede los 200 ms
        if ping_time > 300:
            current_mode = get_current_mode()
            print(f"Modo actual: {current_mode}")
            
            if current_mode != 4:  # Verifica si no está en modo HOLD (ajustar si el ID es diferente)
                print("Ping alto, cambiando el estado a HOLD...")
                set_mode("HOLD")  # Cambiar a modo HOLD
            else:
                print("Ya está en modo HOLD.")
        else:
            print("Ping en rango aceptable.")
    else:
        if current_mode != 4:  # Verifica si no está en modo HOLD (ajustar si el ID es diferente)
            print("Ping alto, cambiando el estado a HOLD...")
            set_mode("HOLD")  # Cambiar a modo HOLD
        else:
            print("Ya está en modo HOLD.")
    
    # Esperar 5 segundos antes de volver a verificar
    time.sleep(5)
