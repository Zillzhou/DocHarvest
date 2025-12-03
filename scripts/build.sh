#!/bin/bash
# 飞书文档爬取工具 - Linux/Mac打包脚本

echo "========================================"
echo "飞书文档爬取工具 - 打包脚本"
echo "========================================"
echo ""

echo "[1/3] 清理旧文件..."
rm -rf build dist "飞书文档爬取工具.spec"

echo ""
echo "[2/3] 开始打包..."
pyinstaller --clean build.spec

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 打包失败！"
    exit 1
fi

echo ""
echo "[3/3] 复制配置文件..."
if [ -f "dist/config.json" ]; then
    echo "✅ 配置文件已包含"
else
    cp config.json dist/
fi

echo ""
echo "========================================"
echo "✅ 打包完成！"
echo "可执行文件位置: dist/飞书文档爬取工具"
echo "========================================"
echo ""

