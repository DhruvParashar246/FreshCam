@echo off
echo ================================================
echo    FreshCam Backend Setup Script
echo ================================================
echo.

REM Check if virtual environment exists
if exist venv (
    echo [√] Virtual environment found
) else (
    echo [i] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [X] Failed to create virtual environment
        echo [!] Make sure Python is installed and in PATH
        pause
        exit /b 1
    )
    echo [√] Virtual environment created
)

echo.
echo [i] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [i] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo [X] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ================================================
echo    Setup Complete!
echo ================================================
echo.
echo Next steps:
echo   1. Run: start_server.bat
echo   2. Visit: http://localhost:8000/docs
echo.
pause
