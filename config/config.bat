@echo off
setlocal

:: Definir variables
set "PYTHON_PATH=C:\Users\USUARIO\AppData\Local\Programs\Python\Python310\python.exe"
set "PROJECT_ROOT=C:\Users\usuario\Desktop\rover-scripts"
set "BASE_IP_RELAY=http://192.168.124.163"
set "TOKEN_PATIO=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDQsInVzZXJuYW1lIjoic2NAdGVzdC5jb20iLCJpYXQiOjE3MjE3NjY5NjgsImV4cCI6MTc1MzMwMjk2OH0.UrIetzHOSBcTlMdeOD_TRyj4eLIHMdzx-SxZXSfwQM4"
set "BASE_URL_PATIO=https://www.patio-driver.patiodelivery2.com"
set "IP_LOCAL_MAVPROXY=127.0.0.1"
set "IP_REMOTE_MAVPROXY=127.0.0.1"
set "PORT_COM_CUBE=COM4"
set "PORT_COM_LIDAR=COM8"
set "MEET_LINK=https://meet.google.com/wph-fjdb-npn"

:: Configurar variables de entorno
echo Configurando variables de entorno...
setx PYTHON_PATH "%PYTHON_PATH%"
setx PROJECT_ROOT "%PROJECT_ROOT%"
setx BASE_IP_RELAY "%BASE_IP_RELAY%"
setx TOKEN_PATIO "%TOKEN_PATIO%"
setx BASE_URL_PATIO "%BASE_URL_PATIO%"
setx IP_LOCAL_MAVPROXY "%IP_LOCAL_MAVPROXY%"
setx IP_REMOTE_MAVPROXY "%IP_REMOTE_MAVPROXY%"
setx PORT_COM_CUBE "%PORT_COM_CUBE%"
setx MEET_LINK "%MEET_LINK%"

echo.
echo Todas las variables de entorno han sido configuradas.
echo Por favor, REINICIA LA TERMINAL y ejecuta el parametro check en `check.bat`.
echo Presiona una tecla para salir.
pause >nul
