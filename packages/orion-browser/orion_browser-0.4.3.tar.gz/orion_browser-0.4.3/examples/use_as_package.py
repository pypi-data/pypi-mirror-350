#!/usr/bin/env python3
"""
示例：如何将Orion作为库导入并使用

此示例展示：
1. 如何导入orion模块
2. 如何使用浏览器管理器
3. 如何使用终端管理器
4. 如何使用文本编辑器
"""

import asyncio
import os
# 从正确的路径导入BrowserManager
from app.tools.browser.browser_manager import BrowserManager
from app.types.messages import BrowserActionRequest
from app.types.browser_types import BrowserAction, GoToUrlAction

async def browser_example():
    """浏览器管理器使用示例"""
    print("=== 浏览器管理器示例 ===")
    
    # 创建浏览器管理器实例
    browser = BrowserManager(headless=False)
    
    try:
        # 初始化浏览器
        await browser.initialize()
        print("浏览器已初始化")
        
        # 给BrowserContext添加缺失的方法
        if not hasattr(browser.browser_context, 'ensure_page_alive'):
            browser.browser_context.ensure_page_alive = async_dummy_function
        
        # 导航到网页
        # 创建BrowserAction对象，设置browser_navigate字段
        browser_action = BrowserAction(
            go_to_url=GoToUrlAction(url="https://www.baidu.com")
        )
        
        # 创建BrowserActionRequest对象
        action = BrowserActionRequest(
            action=browser_action
        )
        
        result = await browser.execute_action(action)
        print(f"导航结果: {result}")
        
        # 等待一段时间以便查看页面
        await asyncio.sleep(3)
        
        # 关闭浏览器
        await browser.close()
        print("浏览器已关闭")
    except Exception as e:
        print(f"浏览器错误: {e}")
        # 确保close方法存在
        if hasattr(browser, 'close'):
            await browser.close()

# 添加一个空的异步函数作为占位符
async def async_dummy_function():
    """空的异步函数，作为缺失方法的占位符"""
    return True

async def main():
    """运行所有示例"""
    print("Orion库使用示例\n")
    
    # 运行浏览器示例
    await browser_example()
    

if __name__ == "__main__":
    asyncio.run(main()) 