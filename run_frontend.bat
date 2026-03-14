@echo off
REM =====================================================
REM Frontend HTTP Server Startup Script for Windows
REM =====================================================

echo.
echo ============================================
echo  Fertilizer Recommendation System
echo  Starting Frontend Server...
echo ============================================
echo.

cd frontend

echo.
echo ============================================
echo  Frontend running on: http://localhost:8080
echo  Make sure backend is running on port 8000
echo  Press Ctrl+C to stop the server
echo ============================================
echo.

python -m http.server 8080

cd ..
pause
