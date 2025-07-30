"""
基于FastMCP的服务器模块
"""

import argparse
import sys
import subprocess
import time
import asyncio
from typing import Any, Dict, List, Union

from mcp.server.fastmcp import FastMCP, Image
from mcp.types import TextContent

from orion_browser_mcp.config import config, update_config_from_args
from orion_browser_mcp.browser_actions import browser_controller
from orion_browser_mcp.utils import format_result


def parse_args():
    """解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(description='浏览器MCP服务器 - FastMCP版本')
    parser.add_argument('--vision', action='store_true', help='启用视觉模式')
    parser.add_argument('--headless', action='store_true', help='以无头模式运行浏览器')
    parser.add_argument('--install-playwright', action='store_true', help='自动安装 playwright 依赖')
    
    args = parser.parse_args()
    return args


def create_server():
    """创建并配置FastMCP服务器
    
    Returns:
        FastMCP: 配置好的服务器实例
    """
    # 解析命令行参数
    args = parse_args()
    
    # 更新配置
    update_config_from_args(args)
    
    # 创建服务器
    mcp = FastMCP(config.server_name)
    
    # 注册工具
    register_tools(mcp)
    
    return mcp




def register_tools(mcp: FastMCP) -> None:
    """注册所有浏览器工具
    
    Args:
        mcp: FastMCP服务器实例
    """
    
    @mcp.tool()
    async def go_url(url: str) -> Union[TextContent, List[Union[TextContent, Image]]]:
        """获取指定网页的基本信息和 element元素内容
        
        Args:
            url: 要获取内容的网址
        """
        result = await browser_controller.go_to_url(url)
        return format_result(result)

    # @mcp.tool()
    # async def browser_install():
    #     """安装 playwright 依赖，只有遇到 playwright 依赖缺失时才会安装"""
    #     print("正在安装 playwright 依赖...")
    #     try:
    #         subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
    #         return "playwright 依赖安装成功！"
    #     except subprocess.CalledProcessError as e:
    #         return f"playwright 依赖安装失败: {e}"

    @mcp.tool()
    async def close_browser():
        """关闭浏览器"""
        result = await browser_controller.close()
        return format_result(result)
        
    @mcp.tool()
    async def open_tab(url: str):
        """打开一个新标签页
        Args:
            url: 要在新标签页中打开的网址
        """
        result = await browser_controller.open_tab(url)
        return format_result(result)
      
    @mcp.tool()
    async def input_text(text: str, index: int):
        """输入文本
        Args:
            text: 要输入的文本
            index: 要输入的element元素的索引
        """
        result = await browser_controller.input_text(text, index)
        return format_result(result)

    @mcp.tool()
    async def click_element(index: int):
        """点击指定索引的element的元素索引
            
        Args:
            index: 要点击的的element元素的索引
        """
        result = await browser_controller.click_element(index)
        return format_result(result)

    @mcp.tool()
    async def go_back():
        """返回上一页
            
        """
        result = await browser_controller.go_back()
        return format_result(result)
    
    @mcp.tool()
    async def switch_tab(page_id: int):
        """切换到指定索引的标签页
            
        Args:
            page_id: 要切换到的标签页的索引
        """
        result = await browser_controller.switch_tab(page_id)
        return format_result(result)

    @mcp.tool()
    async def get_all_tabs():
        """获取所有浏览器标签页

        """
        result = await browser_controller.get_all_tabs()
        return format_result(result)

    @mcp.tool()
    async def done():
        """任务完成"""
        result = await browser_controller.close()
        return format_result("任务完成")
      
    @mcp.tool()
    async def send_keys(keys: str):
        """发送特殊按键字符串，如Escape、Backspace、Insert、PageDown、Delete、Enter等
        
        还支持组合键如`Control+o`、`Control+Shift+T`等
        """
        result = await browser_controller.send_keys(keys)
        return format_result(result)

    @mcp.tool()
    async def scroll_down(amount: int):
        """向下滚动页面
        
        Args:
            amount: 滚动的像素数量
        """
        result = await browser_controller.scroll_down(amount)
        return format_result(result)
    
    @mcp.tool()
    async def scroll_down_element(index: int):
        """向下滚动指定索引的 SCROLL Element元素到页面底部
        
        Args:
            index: 要滚动的element元素的索引
        """
        result = await browser_controller.scroll_element_to_bottom_by_index(index)
        return format_result(result)
    

    @mcp.tool()
    async def scroll_up(amount: int):
        """向上滚动页面
        
        Args:
            amount: 滚动的像素数量
        """
        result = await browser_controller.scroll_up(amount)
        return format_result(result)

    @mcp.tool()
    async def scroll_to_text(text: str):
        """滚动到包含特定文本的元素
        
        Args:
            text: 要查找的文本
        """
        result = await browser_controller.scroll_to_text(text)
        return format_result(result)
        
    @mcp.tool()
    async def extract_content():
        """提取页面完整内容，包括所有文本、图片、链接等信息"""
        result = await browser_controller.extract_content()
        return format_result(result)
    
    @mcp.tool()
    async def get_screenshot():
        """获取当前页面截图"""
        result = await browser_controller.extract_content()
        return format_result(result, only_Image=True)
        
    @mcp.tool()
    async def click_by_position(x: int, y: int):
        """通过坐标点击页面
        
        Args:
            x: X坐标
            y: Y坐标
        """
        result = await browser_controller.click_by_position(x, y)
        return format_result(result)
    
    @mcp.tool()
    async def web_search(query: str):
        """在浏览器中搜索指定内容
        
        Args:
            query: 要搜索的内容
        """
        result = await browser_controller.web_search(query)
        return format_result(result)
    
   

def main():
    """主函数，创建并运行服务器"""
    server = create_server()
    server.run(transport='stdio')


if __name__ == "__main__":
    main() 