@echo off
set FLASK_APP=routes.py
set FLASK_ENV=development
for /f "delims=[] tokens=2" %%a in ('ping -4 -n 1 %ComputerName% ^| findstr [') do set LOCAL_IP=%%a
flask run -h %LOCAL_IP%
exit
