@echo off
echo ========================================
echo Quick Orders System Installer
echo ========================================
echo.

echo 1. Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Virtual environment creation failed
    pause
    exit /b 1
)
echo.
echo 2. Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo Virtual environment activation failed
    pause
    exit /b 1
)
echo.
echo 3. Installing Python dependencies...
pip install -r requirements-simple.txt
if errorlevel 1 (
    echo Dependency installation failed, please check Python environment
    pause
    exit /b 1
)

echo.
echo 4. Creating environment configuration file...
if not exist .env (
    copy env.example .env
    echo Created .env configuration file
) else (
    echo .env file already exists
)

echo.
echo 5. Initializing database...
python setup_database.py
if errorlevel 1 (
    echo Database initialization failed, please check MySQL connection
    echo Ensure MySQL service is running and quick-orders database is created
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Start system:
echo   venv\Scripts\activate
echo   python run.py
echo.
echo Access URLs:
echo   Frontend: http://localhost:5000
echo   Admin Panel: http://localhost:5000/admin
echo.
echo Default admin account:
echo   Email: admin@example.com
echo   Password: admin123
echo.
echo ========================================
pause
