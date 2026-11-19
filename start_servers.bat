@echo off
echo ========================================================
echo Starting Polcy AI: SKASC Policy Document Chatbot
echo Backend: Django 6.1 (Port 8000)
echo Frontend: React + Vite (Port 5173)
echo ========================================================

start "Polcy AI Backend (Django)" cmd /k "cd /d %~dp0backend && python manage.py runserver 0.0.0.0:8000"
timeout /t 3 /nobreak >nul
start "Polcy AI Frontend (React)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo Servers started!
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000/api/
pause
