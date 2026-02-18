@echo off
start "Backend (port 8000)" cmd /k "cd /d %~dp0backend && ..\.venv\Scripts\activate.bat && ..\.venv\Scripts\python main.py"
start "Frontend (port 3000)" cmd /k "cd /d %~dp0frontend && npm run dev"
echo.
echo ========================================
echo   RVCE OMR Started
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo ========================================
echo.
pause
