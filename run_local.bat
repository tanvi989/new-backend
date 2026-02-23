@echo off
cd /d "%~dp0"
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Starting backend on http://localhost:5000 ...
python app.py
