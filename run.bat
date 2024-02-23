@ECHO OFF
cd /d %~dp0
start frontend\run.bat
call backend\run.bat
