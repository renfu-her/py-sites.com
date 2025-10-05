@echo off
echo ========================================
echo Quick Orders Flask Server Startup
echo ========================================

REM Change to the script directory
cd /d "%~dp0"

echo Current directory: %CD%

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\activate && pip install -r requirements.txt
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Checking Python environment...
python -c "import sys; print('Python executable:', sys.executable)"

echo.
echo Checking Flask installation...
python -c "import flask; print('Flask version:', flask.__version__)" 2>nul
if errorlevel 1 (
    echo ERROR: Flask not found! Installing dependencies...
    pip install -r requirements.txt
    echo.
    echo Re-checking Flask installation...
    python -c "import flask; print('Flask version:', flask.__version__)"
    if errorlevel 1 (
        echo ERROR: Failed to install Flask!
        pause
        exit /b 1
    )
)

echo.
echo Starting Flask application...
echo Access URL: http://localhost:5000
echo Admin Panel: http://localhost:5000/backend
echo Default Admin: admin@example.com / admin123
echo.
echo Press Ctrl+C to stop the server
echo ========================================

REM Start the Flask application
python app.py

echo.
echo Server stopped.
pause


