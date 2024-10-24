@echo off
cd "C:\Program Files (x86)\MAVProxy"
mavproxy.exe --master=%PORT_COM_CUBE% --logfile=%PROJECT_ROOT%\logs\mav.tlog --out=udp:%IP_REMOTE_MAVPROXY%:14550 --out=udp:%IP_LOCAL_MAVPROXY%:14551
