@echo off
echo ========================================
echo Quick Orders System Starter
echo ========================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)
echo.
echo Starting Quick Orders System...
echo.
python run.py


