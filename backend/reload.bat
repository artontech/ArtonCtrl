@ECHO OFF
cd /d %~dp0
uvicorn server:app --reload --host 0.0.0.0 --port 13314
pause