@echo off
title Install Dependencies
cls

echo ========================================
echo Installing Dependencies
echo ========================================
echo.

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo Error: Python not found!
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Installing packages...
echo.

pip install PyQt5 requests -i https://pypi.tuna.tsinghua.edu.cn/simple

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Installation Complete!
    echo ========================================
    echo.
    echo You can now run: run.bat
    echo Or: python main.py
    echo.
) else (
    echo.
    echo Installation failed!
    echo Try: pip install PyQt5 requests
    echo.
)

pause

