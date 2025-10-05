# Quick Orders Flask Server Startup Script (PowerShell)
Write-Host "========================================" -ForegroundColor Green
Write-Host "Quick Orders Flask Server Startup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Change to the script directory
Set-Location $PSScriptRoot
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Red
    Write-Host "Then run: venv\Scripts\Activate.ps1; pip install -r requirements.txt" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Checking Python environment..." -ForegroundColor Yellow
python -c "import sys; print('Python executable:', sys.executable)"

Write-Host ""
Write-Host "Checking Flask installation..." -ForegroundColor Yellow
try {
    $flaskVersion = python -c "import flask; print(flask.__version__)"
    Write-Host "Flask version: $flaskVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Flask not found! Installing dependencies..." -ForegroundColor Red
    pip install -r requirements.txt
    Write-Host ""
    Write-Host "Re-checking Flask installation..." -ForegroundColor Yellow
    try {
        $flaskVersion = python -c "import flask; print(flask.__version__)"
        Write-Host "Flask version: $flaskVersion" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to install Flask!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "Starting Flask application..." -ForegroundColor Green
Write-Host "Access URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Admin Panel: http://localhost:5000/backend" -ForegroundColor Cyan
Write-Host "Default Admin: admin@example.com / admin123" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

# Start the Flask application
python app.py

Write-Host ""
Write-Host "Server stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"


