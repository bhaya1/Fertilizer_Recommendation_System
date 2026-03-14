@echo off
REM =====================================================
REM FastAPI Backend Startup Script for Windows
REM =====================================================

echo.
echo ============================================
echo  Fertilizer Recommendation System
echo  Starting Backend Server...
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -q -r requirements.txt
echo.

REM Start backend server
echo.
echo ============================================
echo  Backend running on: http://localhost:8000
echo  API Documentation: http://localhost:8000/docs
echo  Press Ctrl+C to stop the server
echo ============================================
echo.

python backend/main.py

pause
