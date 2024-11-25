@echo off

rem Configurar locale
set LANG=en_US.UTF-8
set LC_ALL=en_US.UTF-8

rem Iniciar el script de Python
rem start "" %PYTHON_PATH% "%PROJECT_ROOT%\scripts\deep_camera.py"

rem Esperar 10 segundos para asegurar que el script se inicia correctamente
timeout /t 10

rem Iniciar OBS Studio
start /d "C:\Program Files\obs-studio\bin\64bit\" "" obs64.exe --startvirtualcam

rem Esperar 10 segundos para que OBS se inicie
timeout /t 10

rem Intentar ping a Google para verificar la conexión a Internet
:checkinternet
ping -n 1 www.google.com >nul
if errorlevel 1 (
    echo No hay conexion a Internet. Reintentando en 5 segundos...
    timeout /t 5 >nul
    goto checkinternet
) else (
    rem echo Conexión a Internet detectada.
    rem Abre la URL de Google Meet en el navegador predeterminado
    rem start "" %MEET_LINK%

    timeout /t 5
    rem Abrir app rover
    start "" "%PROJECT_ROOT%\rover-app\rover_relay.exe"
    
    rem timeout /t 5
    rem Iniciar MAVProxy
    rem start "" "%PROJECT_ROOT%\scripts\mavproxy_start.bat"

    timeout /t 5
    rem Iniciar MAVProxy
    start "" "%PROJECT_ROOT%\scripts\start_wsl.bat"

    timeout /t 10
    rem Iniciar server
    start "" %PYTHON_PATH% "%PROJECT_ROOT%\commands\main.py"

    timeout /t 10
    rem Iniciar Lidar
    start "" %PYTHON_PATH% "%PROJECT_ROOT%\commands\lidar_client.py"

    rem timeout /t 10
    rem Iniciar Sonar
    rem start "" %PYTHON_PATH% "%PROJECT_ROOT%\commands\sonar_client.py"

    timeout /t 10
    rem Iniciar ping to ip
    start "" %PYTHON_PATH% "%PROJECT_ROOT%\scripts\latency.py"

    rem timeout /t 10
    rem Iniciar nextion display
    rem start "" %PYTHON_PATH% "%PROJECT_ROOT%\scripts\nextion_data.py"
)
