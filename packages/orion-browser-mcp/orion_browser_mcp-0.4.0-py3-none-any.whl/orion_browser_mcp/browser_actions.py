"""
浏览器操作模块
"""

from typing import Dict, Any

from orion_browser import (
    BrowserManager, BrowserActionRequest, BrowserAction,
    GoToUrlAction, OpenTabAction, InputTextAction, ClickElementAction,
    SwitchTabAction, SendKeysAction, ScrollAction, ScrollToTextAction,
    ExtractPageContentAction, ClickByPositionAction, GetAllTabsAction, NoParamAction
)

from orion_browser_mcp.config import config


class BrowserController:
    """浏览器控制器类，封装浏览器操作"""

    def __init__(self):
        """初始化浏览器控制器"""
        self.browser = None
        self.initialized = False

    async def get_browser(self) -> BrowserManager:
        """获取浏览器管理器实例，如果未初始化则进行初始化
        
        Returns:
            BrowserManager: 浏览器管理器实例
        """
        if not self.initialized:
            await self.initialize()
        return self.browser

    async def initialize(self) -> None:
        """初始化浏览器管理器"""
        if not self.initialized:
            self.browser = BrowserManager(
                headless=config.headless,
                highlight_elements=config.highlight_elements
            )
            await self.browser.initialize()
            self.initialized = True

    async def close(self) -> Dict[str, Any]:
        """关闭浏览器
        
        Returns:
            Dict: 包含操作结果的字典
        """
        if self.initialized and self.browser:
            await self.browser.close()
            self.initialized = False
            return {"status": "success", "message": "浏览器已关闭"}
        return {"status": "info", "message": "浏览器已经关闭或未初始化"}

    async def go_to_url(self, url: str) -> Dict[str, Any]:
        """导航到指定URL
        
        Args:
            url: 要访问的URL
            
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    go_to_url=GoToUrlAction(url=url)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            await self.close()
            return {"status": "error", "message": str(e)}
        

    async def open_tab(self, url: str) -> Dict[str, Any]:
        """打开新标签页
        
        Args:
            url: 要在新标签页中打开的URL
            
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    open_tab=OpenTabAction(url=url)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def input_text(self, text: str, index: int) -> Dict[str, Any]:
        """在输入框中输入文本
        
        Args:
            text: 要输入的文本
            index: 输入框索引
            
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    input_text=InputTextAction(text=text, index=index)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def click_element(self, index: int) -> Dict[str, Any]:
        """点击元素
        
        Args:
            index: 要点击的元素索引
            
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    click_element=ClickElementAction(index=index)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def switch_tab(self, page_id: int) -> Dict[str, Any]:
        """切换标签页
        
        Args:
            page_id: 要切换到的标签页ID
            
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    switch_tab=SwitchTabAction(page_id=page_id)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    async def get_all_tabs(self) -> Dict[str, Any]:
        """获取所有浏览器标签页
        
        Args:
            page_id: 要切换到的标签页ID
            
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    get_all_tabs=GetAllTabsAction()
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def send_keys(self, keys: str) -> Dict[str, Any]:
        """发送键盘输入
        
        Args:
            keys: 要发送的键，如Escape、Backspace、Insert、PageDown、Delete、Enter等，
                  也支持组合键如Control+o、Control+Shift+T
                  
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    send_keys=SendKeysAction(keys=keys)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def scroll_down(self, amount: int) -> Dict[str, Any]:
        """向下滚动页面
        
        Args:
            amount: 滚动的像素数量
            
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    scroll_down=ScrollAction(amount=amount)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    async def scroll_element_to_bottom_by_index(self, index: int) -> Dict[str, Any]:
        """滚动指定索引的element元素到页面底部
        
        Args:
            index: 要滚动的element元素的索引
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    scroll_element_to_bottom_by_index=ScrollAction(index=index)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def go_back(self) -> Dict[str, Any]:
        """返回上一页
        
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    go_back=ExtractPageContentAction()
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def scroll_up(self, amount: int) -> Dict[str, Any]:
        """向上滚动页面
        
        Args:
            amount: 滚动的像素数量
            
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    scroll_up=ScrollAction(amount=amount)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def scroll_to_text(self, text: str) -> Dict[str, Any]:
        """滚动到包含特定文本的元素
        
        Args:
            text: 要查找的文本
            
        Returns:
            Dict: 包含操作结果的字典
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    scroll_to_text=ScrollToTextAction(text=text)
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def extract_content(self) -> Dict[str, Any]:
        """提取页面内容以从页面中检索特定信息，例如所有公司名称、特定描述、有关的所有信息、结构化格式的公司链接或简单链
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    extract_content=ExtractPageContentAction()
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    async def web_search(self, query: str) -> Dict[str, Any]:
        """在浏览器中搜索指定内容
        
        Args:
            query: 要搜索的内容
        """
        try:
            await self.initialize()
            action = BrowserActionRequest(
                action=BrowserAction(
                    go_to_url=GoToUrlAction(url=f"https://cn.bing.com/search?q={query}")
                )
            )
            return await self.browser.execute_action(action)
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
        

    # async def click_by_position(self, x: int, y: int) -> Dict[str, Any]:
    #     """通过坐标点击页面
        
    #     Args:
    #         x: X坐标
    #         y: Y坐标
            
    #     Returns:
    #         Dict: 包含操作结果的字典
    #     """
    #     try:
    #         await self.initialize()
    #         action = BrowserActionRequest(
    #             action=BrowserAction(
    #                 click_by_position=ClickByPositionAction(x=x, y=y)
    #             )
    #         )
    #         return await self.browser.execute_action(action)
    #     except Exception as e:
    #         return {"status": "error", "message": str(e)}
            
# 创建全局浏览器控制器实例
browser_controller = BrowserController() 