#!/bin/bash

# Definir variables de entorno si es necesario
export SESSION_NAME="mavproxy_session"
export PORT_COM_CUBE="COM4"
export IP_LOCAL_MAVPROXY="127.0.0.1"
export IP_REMOTE_MAVPROXY="127.0.0.1"
export PROJECT_ROOT_WSL="/mnt/c/Users/usuario/Desktop/rover-scripts/dev"

# Nombre de la sesión de screen
# session_name="mavproxy_session"

# Comando para ejecutar mavproxy
mavproxy_command="mavproxy.exe --master=$PORT_COM_CUBE --out=udp:$IP_LOCAL_MAVPROXY:14551 --out=udp:$IP_REMOTE_MAVPROXY:14550 --logfile=$PROJECT_ROOT_WSL/logs/mav.tlog"
# mavproxy_command="mavproxy.exe --master=$PORT_COM_CUBE"

# Crear y nombrar una sesión de screen, ejecutar el comando en la sesión
screen -dmS "$SESSION_NAME" bash -c "$mavproxy_command"

# screen -r mavproxy_session