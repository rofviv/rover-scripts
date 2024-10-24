import os
import subprocess
import time
from pymavlink import mavutil
import threading

session_name = os.getenv('SESSION_NAME', "mavproxy_session")
ip_local_mavproxy = os.getenv('IP_LOCAL_MAVPROXY', '0.0.0.0')
host_to_ping = os.getenv('IP_REMOTE_MAVPROXY', '192.168.18.20')
connection_string = f"udp:{ip_local_mavproxy}:14551"
master = mavutil.mavlink_connection(connection_string)

def send_command_to_wsl(command):
    wsl_command = f'screen -S {session_name} -p 0 -X stuff "{command}\\n"'
    subprocess.run(f'wsl {wsl_command}', shell=True)

def execute_commands():
    print("Send command")
    commands = [
        'rc 2 2000',
        'rc 2 0',
        # 'mode hold',
    ]
    
    for command in commands:
        send_command_to_wsl(command)

def execute_commands_in_thread():
    command_thread = threading.Thread(target=execute_commands)
    command_thread.start()

# Función para verificar el ping con un timeout para evitar bloqueos
def check_ping(host):
    try:
        # Añadir el parámetro "-w" para que el comando tenga un tiempo máximo de espera (timeout)
        output = subprocess.check_output(["ping", "-n", "1", "-w", "2000", host], timeout=1.5)
        lines = output.decode().strip().split("\n")
        for line in lines:
            if "time=" in line:
                time_ms = line.split("time=")[-1].split(" ")[0]
                time_ms = float(time_ms.replace('ms', ''))
                return time_ms
    except subprocess.CalledProcessError:
        print(f"No se puede hacer ping a {host}.")
    except subprocess.TimeoutExpired:
        print(f"Tiempo de espera de ping agotado para {host}.")
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
    master.wait_heartbeat()
    print("Conectado al vehículo.")

    system_id = master.target_system
    component_id = master.target_component
    
    mode_mapping = {
        'HOLD': 4,  # ID del modo HOLD (ajustar según sea necesario)
    }
    
    if mode in mode_mapping:
        mode_id = mode_mapping[mode]
        print(f"Cambiando a modo {mode}...")
        master.mav.set_mode_send(
            system_id,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id
        )
        print(f"Modo cambiado a {mode}.")
    else:
        print("Modo no reconocido.")

while True:
    ping_time = check_ping(host_to_ping)
    
    if ping_time is not None:
        print(f"Ping a {host_to_ping}: {ping_time} ms")
        
        if ping_time > 300:
            current_mode = get_current_mode()
            print(f"Modo actual: {current_mode}")
            
            if current_mode != 4:  # Verifica si no está en modo HOLD
                print("Ping alto, cambiando el estado a HOLD...")
                set_mode("HOLD")  # Cambiar a modo HOLD
            else:
                print("Ya está en modo HOLD.")
        else:
            print("Ping en rango aceptable.")
    else:
        print("Conexión perdida, ejecutando comandos...")
        execute_commands_in_thread()  # Ejecutar comandos si no hay conexión
    
    # Esperar 1 segundos antes de volver a verificar 
    time.sleep(1) 
