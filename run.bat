@echo off
echo ========================================
echo   Multifolks Backend Server
echo ========================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo.
    echo Virtual environment created and dependencies installed!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Run the server
echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause

