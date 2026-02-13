@echo off
REM Single-window start for backend and frontend; activates .venv for backend
SETLOCAL

REM Directory of this script (includes trailing backslash)
SET SCRIPT_DIR=%~dp0

REM Start backend in background in the same console, activating the .venv first
start /B "" cmd /c "call "%SCRIPT_DIR%\.venv\Scripts\activate.bat" && pushd "%SCRIPT_DIR%backend" && python main.py"

REM Start frontend in background in the same console from the frontend folder
start /B "" cmd /c "pushd "%SCRIPT_DIR%frontend" && npm run dev"

echo Servers started (logs will be interleaved here). Press any key to stop.

REM Keep the window open so outputs remain visible until the user closes it
pause   

ENDLOCAL

REM Exit the original script
exit /b 0
