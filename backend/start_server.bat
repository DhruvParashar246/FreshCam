@echo off
echo ================================================
echo    Starting FreshCam Backend Server
echo ================================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [√] Virtual environment activated
) else (
    echo [!] Virtual environment not found
    echo [!] Run setup.bat first
    pause
    exit /b 1
)

echo.
echo [i] Starting FastAPI server on http://localhost:8000
echo [i] API docs available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app:app --reload --host 0.0.0.0 --port 8000
