"""
通用工具函数模块
"""

import base64
import json
from io import BytesIO
from typing import Any, Dict, List, Union

from PIL import Image as PILImage
from mcp.types import TextContent, ImageContent as McpImage
from mcp.server.fastmcp import Image
from orion_browser_mcp.config import config


def screenshot_base64(screenshot_path: str, quality: int = None, max_size: tuple = None) -> str:
    """将图片文件压缩并转换为base64编码
    
    Args:
        screenshot_path: 图片文件路径
        quality: 压缩质量，1-100之间的整数，默认使用配置值
        max_size: 图片的最大尺寸，超过将等比例缩小，默认使用配置值
        
    Returns:
        base64编码的字符串
    """
    # 使用默认配置或者传入的参数
    quality = quality if quality is not None else config.image_quality
    max_size = max_size or (config.max_image_width, config.max_image_height)
    
    try:
        # 打开图片
        img = Image.open(screenshot_path)
        
        # 调整图片大小，保持宽高比
        if img.width > max_size[0] or img.height > max_size[1]:
            img.thumbnail(max_size, Image.LANCZOS)
        
        # 将图片保存到内存中
        buffer = BytesIO()
        img_format = img.format if img.format else 'JPEG'
        img.save(buffer, format=img_format, quality=quality, optimize=True)
        
        # 将图片转换为base64编码
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return img_str
    except Exception as e:
        print(f"图片转换失败: {str(e)}")
        return None


def format_result(result: Any, only_Image: bool = False) -> Union[TextContent, List[Union[TextContent, McpImage]]]:
    """将结果格式化为MCP返回格式
    
    Args:
        result: 任意类型的结果对象
        
    Returns:
        格式化后的MCP内容对象
    """
    if config.json_format and not only_Image:
        # 处理不能直接序列化的对象
        try:
            # 如果是对象实例，先转换为字典
            if hasattr(result, '__dict__'):
                result_dict = result.__dict__
                return TextContent(type="text", text=json.dumps(result_dict, indent=2, ensure_ascii=False))
            else:
                return TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))
        except (TypeError, AttributeError) as e:
            # 如果序列化失败，返回字符串表示
            return TextContent(type="text", text=str(result))
    
    if hasattr(result, '__dict__'):  # 处理类实例
        try:
            # 尝试将类实例转为字典
            obj_dict = result.__dict__
            
            # 构建格式化文本输出
            formatted_text = ""
            for key, value in obj_dict.items():
                if key not in ["clean_screenshot_path", "screenshot_uploaded", "clean_screenshot_uploaded", "error"]:
                    value_str = (json.dumps(value, indent=2, ensure_ascii=False) 
                                if isinstance(value, (dict, list, tuple)) 
                                else str(value))
                    formatted_text += f"#### {key}\n\n{value_str}\n\n"
            
            # 创建文本内容
            text_content = TextContent(type="text", text=formatted_text)
            
            # 如果启用了视觉模式并且有截图，则同时返回图片和文本
            if (config.vision_enabled and "clean_screenshot_path" in obj_dict and obj_dict["clean_screenshot_path"]) or only_Image: 
                img = PILImage.open(obj_dict["clean_screenshot_path"])
                img.thumbnail((800, 800))
                buffer = BytesIO()
                img.save(buffer, format="PNG", optimize=True, quality=75)
                buffer.seek(0)
                
                # 创建图片内容
                image_content = Image(data=buffer.getvalue(), format="png")
                
                # 返回图片和文本的列表
                if only_Image:
                    return [image_content]
                else:
                    return [image_content, text_content]
            else:
                # 只返回文本内容
                return text_content
                
        except Exception as e:
            # 如果无法获取属性，返回错误信息
            return TextContent(type="text", text=f"#### 结果处理错误\n\n{str(e)}")
    elif isinstance(result, str):
        return TextContent(type="text", text=result)
    else:
        return TextContent(type="text", text=f"### 结果\n\n{str(result)}") 