@echo off
echo Starting Quick Orders Flask Application...
echo.

REM Change to the project directory
cd /d "%~dp0"

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if Flask is available
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ERROR: Flask not found in virtual environment!
    echo Please run: venv\Scripts\activate && pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Starting Flask application...
echo Access URL: http://localhost:5000
echo Admin Panel: http://localhost:5000/backend
echo Default Admin: admin@example.com / admin123
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python app.py

pause


