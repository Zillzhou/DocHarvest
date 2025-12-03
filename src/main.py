"""
飞书文档爬取工具 - 主程序入口
Author: Python Engineer
Version: 1.0.0
Description: 从飞书分享链接中获取文档内容并导出为Markdown文件
"""

import sys
import os

# 确保能找到模块（特别是打包后）
if getattr(sys, 'frozen', False):
    # 如果是PyInstaller打包的exe
    application_path = sys._MEIPASS
else:
    # 如果是普通Python运行
    application_path = os.path.dirname(os.path.abspath(__file__))

# 添加到系统路径
sys.path.insert(0, application_path)

from apple_gui import run_apple_app


def main():
    """主函数"""
    try:
        run_apple_app()
    except Exception as e:
        print(f"程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")


if __name__ == '__main__':
    main()

