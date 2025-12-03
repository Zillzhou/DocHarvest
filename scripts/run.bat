@echo off
cd /d "%~dp0\.."
chcp 65001 >nul
title DocHarvest - 飞书文档导出工具
cls

echo ========================================
echo DocHarvest - 飞书文档导出工具
echo ========================================
echo.
echo 正在启动...
echo.

python src\main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 启动失败！
    echo.
    echo 请检查:
    echo   1. 是否已安装 Python 3.9+
    echo   2. 是否已安装依赖: pip install -r requirements.txt
    echo   3. 是否在项目根目录运行
    echo.
    pause
)

