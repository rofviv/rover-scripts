@echo off
rem Cambia el puerto y la velocidad de baudios según tu configuración
@REM set PYTHONPATH=%PYTHONPATH%;c:/Users/BOT/Desktop/rover-scripts/dev/modules
mavproxy.exe --master=COM4 --baudrate 115200 --cmd="module load simple_module"
