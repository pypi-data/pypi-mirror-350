"""
主模块入口点
"""

import argparse
import sys
import subprocess
import os

from orion_browser_mcp.config import config, update_config_from_args


def parse_args():
    """解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(description='浏览器MCP服务器')
    
    # 基本配置
    parser.add_argument('--vision', action='store_true', help='启用视觉模式')
    parser.add_argument('--headless', action='store_true', help='以无头模式运行浏览器')
    parser.add_argument('--install-playwright', action='store_true', help='自动安装 playwright 依赖')
    
    args = parser.parse_args()
    return args


def install_playwright():
    """安装 playwright 依赖"""
    print("正在安装 playwright 依赖...")
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("playwright 依赖安装成功！")
    except subprocess.CalledProcessError as e:
        print(f"playwright 依赖安装失败: {e}")
        sys.exit(1)


def main():
    # 解析命令行参数
    args = parse_args()
    
    # 如果指定了安装 playwright 选项
    if args.install_playwright:
        install_playwright()
    
    # 自动检测是否需要安装 playwright
    try:
        # 尝试导入 playwright 以检查是否已安装
        from playwright.sync_api import sync_playwright
    except ImportError:
        # 如果没有安装，提示用户
        print("检测到 playwright 未安装。添加 --install-playwright 参数可自动安装 playwright 依赖。")
        print("例如: uvx orion-browser-mcp --install-playwright")
    
    # 更新配置
    update_config_from_args(args)
    
    from orion_browser_mcp.server.fast_server import main as fast_main
    fast_main()
        
   


if __name__ == "__main__":
    main() 