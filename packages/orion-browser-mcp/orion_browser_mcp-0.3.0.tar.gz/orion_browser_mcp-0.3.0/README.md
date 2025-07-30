# Orion Browser MCP

基于Orion浏览器的MCP (Machine Communicatin Protocol) 服务，提供浏览器自动化控制能力。

## 功能特点

- 支持FastMCP和SSE两种服务模式
- 提供完整的浏览器控制API，包括导航、点击、输入等操作
- 支持截图和视觉模式
- 完善的错误处理和日志记录
- 模块化设计，易于扩展

## 安装

### 要求

- Python 3.12+
- 依赖项: 见 `pyproject.toml`

### 步骤

1. 克隆代码库
2. 进入项目目录
3. 创建虚拟环境: `python -m venv .venv`
4. 激活虚拟环境:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
5. 安装依赖: `pip install -e .`

## 使用方法

### 基本用法

```bash
# 启动FastMCP服务器(默认)
python main.py

# 启用视觉模式
python main.py --vision

# 无头模式
python main.py --headless


### API参考

服务器提供以下工具:

- `go_url`: 导航到指定URL
- `open_tab`: 打开新标签页
- `input_text`: 在元素中输入文本
- `click_element`: 点击指定元素
- `switch_tab`: 切换标签页
- `close_browser`: 关闭浏览器
- `send_keys`: 发送键盘输入
- `scroll_down`/`scroll_up`: 页面滚动
- `scroll_to_text`: 滚动到包含特定文本的元素
- `extract_content`: 提取页面内容
- `click_by_position`: 通过坐标点击页面

## 项目结构

```
orion_browser_mcp/
├── __init__.py           # 包初始化文件
├── __main__.py           # 主入口点
├── config.py             # 配置管理
├── utils.py              # 通用工具函数
├── browser_actions.py    # 浏览器操作封装
├── server/               # 服务器实现
│   ├── __init__.py
│   ├── fast_server.py    # FastMCP服务器
```

## 贡献

欢迎通过Issue和Pull Request贡献代码和反馈问题。

## 许可

[LICENSE]
