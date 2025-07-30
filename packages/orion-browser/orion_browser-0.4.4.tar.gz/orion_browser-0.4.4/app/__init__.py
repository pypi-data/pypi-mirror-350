"""
Orion: 终端与浏览器代理服务器

该模块提供了终端模拟器和浏览器代理功能，可以用作独立服务或导入为Python包使用。
"""

# 导出主要组件供包导入
from app.server import app
from app.tools.browser.browser_manager import BrowserManager

__version__ = "0.1.0"

# 创建函数用于启动服务器
def create_app():
    """创建并返回FastAPI应用实例"""
    return app

async def start_server(host="0.0.0.0", port=8330, log_level="info", chrome_path=None, reload=False):
    """
    启动Orion服务器

    Args:
        host (str): 服务器绑定的主机地址
        port (int): 服务器端口
        log_level (str): 日志级别
        chrome_path (str, optional): Chrome浏览器路径
        reload (bool): 是否启用自动重载（开发模式）
    """
    import uvicorn
    from app.logger import logger
    import os
    
    # 设置Chrome实例路径（如果提供）
    if chrome_path:
        os.environ['CHROME_INSTANCE_PATH'] = chrome_path
        
    # 记录启动信息
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Log level: {log_level}")
    logger.info(f"CHROME_INSTANCE_PATH env is {os.getenv('CHROME_INSTANCE_PATH', 'empty')}")
    if reload:
        logger.info("Auto-reload enabled (development mode)")

    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level=log_level,
        reload=reload
    )

    server = uvicorn.Server(config)
    await server.serve()

# 导出核心功能
__all__ = [
    "app", 
    "BrowserManager", 
    "start_server"
]
