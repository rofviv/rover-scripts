## ROVER CONFIG
#### Instala los programas de la carpeta programs
#### Preparar el archivo config/config.bat
1.- Tener instalado python (en este ejemplo 3.10.0) y en una terminal ejecuta pip install -r requirements.txt

2.- Ejecutar en CMD (WIN + R): where python (o python3)
    - C:\Users\BOT\AppData\Local\Programs\Python\Python312\python.exe
    El resultado pegar en la variable PYTHON_PATH de config.bat

3.- Setear la variable ROOT_PROJECT (Lugar de la carpeta de este proyecto)
    - Ejecutar: pwd (C:\Users\BOT\Desktop\rover-scripts)
    - Copiar y pegar en la variable ROOT_PROJECT

4.- Configura la IP del Relay (Tambien se puede actualizar desde la app rover)
    - Desde el hotspot o router revisa la IP del realy y setealo en BASE_IP_RELAY: http://192.168.124.163

5.- Opcionalmente, configura la URL BASE del servidor Patio y el token. (Se puede cambiar desde la app rover)

6.- Configurar IP_LOCAL_MAVPROXY abre el programa wireguard y conectate a la vpn configurada previamente. Copia la ip que te proporciana la configuracion
    - 10.13.13.3

7.- Configurar IP_REMOTE_MAVPROXY Esto se obtiene de la PC que controlara el rover. Abre wireguard en la otra PC y escribe la ip que te proporciona el sistema
    - 10.13.13.2

8.- Configurar el puerto COM del cube. Identifica el puerto COM cuando conectas el cube a la computadora
    - Setea el valor en la variable PORT_COM_CUBE (en este ejemplo es el COM3)

9.- Setea el link que se usara para la camara del rover. Se debe tener creada una reunion abierta en meet
    - Setea el valor en MEET_LINK (En este ejemplo: https://meet.google.com/wph-fjdb-npn)

10.- Abre la terminal (Windows terminal) y ejecuta el archivo ./config/config.bat luego reinicia la consola y ejecuta ./check.bat para revisar las configuraciones

-----------------------------
### Configuraciones adicionales

### Inicio automatico
- En el administrador de tareas permitir Anydesk que se ejecute al inicio
- WIN + R -> shell:startup -> crear acceso directo a scripts/rover_launcher.bat (Recomendacion: Ejecutar el archivo .bat localmente antes de automatizar)
- Tambien crear un acceso directo a wireguard en el inicio

##### Configurar WIFI. conectar automaticamente
ssid: OMEN-PC
pass: Pass123!

Instalar Anydesk 
Instalar OBS
Instalar Wireguard
Instalar Mavproxy
Instalar Python
Instalar VSC
Instalar Drivers Lidar https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads