@echo off
chcp 65001
echo ========================================
echo 飞书文档爬取工具 - 打包脚本
echo ========================================
echo.

echo [1/3] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "飞书文档爬取工具.spec" del "飞书文档爬取工具.spec"

echo.
echo [2/3] 开始打包...
pyinstaller --clean build.spec

if %errorlevel% neq 0 (
    echo.
    echo ❌ 打包失败！
    pause
    exit /b 1
)

echo.
echo [3/3] 复制配置文件...
if exist dist\config.json (
    echo ✅ 配置文件已包含
) else (
    copy config.json dist\
)

echo.
echo ========================================
echo ✅ 打包完成！
echo 可执行文件位置: dist\飞书文档爬取工具.exe
echo ========================================
echo.

pause

