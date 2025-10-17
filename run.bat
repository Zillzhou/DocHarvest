@echo off
title Feishu Document Crawler
cls

echo ========================================
echo Feishu Document Crawler
echo ========================================
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Program failed to start!
    echo.
    echo Please check:
    echo   1. Python is installed
    echo   2. Dependencies are installed: pip install PyQt5 requests
    echo.
    pause
)

