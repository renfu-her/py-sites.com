#!/usr/bin/env python3
"""
Environment Test Script for Quick Orders Flask Application
This script helps diagnose Python environment issues.
"""

import sys
import os
import subprocess

def main():
    print("=" * 60)
    print("Quick Orders Flask Environment Test")
    print("=" * 60)
    
    # Check Python version and path
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.path}")
    
    # Check virtual environment
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        print(f"Virtual environment: {venv_path}")
    else:
        print("Virtual environment: NOT ACTIVATED")
    
    # Check if we're in the right directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Check for required files
    required_files = ['app.py', 'application.py', 'requirements.txt', 'venv']
    print("\nRequired files check:")
    for file in required_files:
        if os.path.exists(file):
            print(f"  [OK] {file}")
        else:
            print(f"  [MISSING] {file}")
    
    # Try to import Flask
    print("\nFlask import test:")
    try:
        import flask
        print(f"  [OK] Flask imported successfully")
        print(f"  [OK] Flask version: {flask.__version__}")
    except ImportError as e:
        print(f"  [FAILED] Flask import failed: {e}")
        
        # Try to check if Flask is installed in venv
        if os.path.exists('venv/Scripts/pip.exe'):
            print("\nChecking Flask installation in virtual environment:")
            try:
                result = subprocess.run(['venv/Scripts/pip.exe', 'list'], 
                                      capture_output=True, text=True)
                if 'Flask' in result.stdout:
                    print("  [OK] Flask is installed in venv")
                else:
                    print("  [FAILED] Flask is NOT installed in venv")
            except Exception as e:
                print(f"  [ERROR] Error checking venv: {e}")
    
    # Try to import other required modules
    print("\nOther required modules test:")
    modules_to_test = [
        'flask_sqlalchemy',
        'flask_migrate', 
        'flask_login',
        'pymysql',
        'PIL'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"  [OK] {module}")
        except ImportError as e:
            print(f"  [FAILED] {module}: {e}")
    
    print("\n" + "=" * 60)
    print("Environment test completed.")
    print("=" * 60)

if __name__ == '__main__':
    main()
