@echo off
echo ========================================
echo   Restart Multifolks Backend (port 5000)
echo ========================================
echo.

cd /d "%~dp0"

REM Kill any process using port 5000 (get PIDs from netstat)
echo Checking port 5000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000"') do (
    echo Killing process %%a on port 5000...
    taskkill /F /PID %%a 2>nul
)
timeout /t 2 /nobreak >nul
echo.
:start

REM Activate venv if present
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist "..\venv\Scripts\activate.bat" (
    call ..\venv\Scripts\activate.bat
)

echo.
echo Starting backend on http://localhost:5000 ...
echo Press Ctrl+C to stop.
echo.
python app.py

pause
