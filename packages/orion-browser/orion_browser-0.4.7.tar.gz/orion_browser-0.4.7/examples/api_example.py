#!/usr/bin/env python3
"""
示例：如何通过API调用使用Orion服务

此示例展示：
1. 如何连接到运行中的Orion服务
2. 如何调用浏览器API
3. 如何调用终端API
4. 如何调用文本编辑器API
"""

import asyncio
import json
import httpx
from websockets.client import connect

API_BASE = "http://localhost:8330"  # Orion服务器基础URL

async def browser_api_example():
    """浏览器API使用示例"""
    print("=== 浏览器API示例 ===")
    
    async with httpx.AsyncClient() as client:
        # 获取浏览器状态
        response = await client.get(f"{API_BASE}/browser/status")
        status = response.json()
        print(f"浏览器状态: {'健康' if status.get('healthy') else '不健康'}")
        
        # 执行浏览器操作（导航到网页）
        browser_action = {
            "action": "navigate",
            "args": {"url": "https://www.baidu.com"}
        }
        response = await client.post(f"{API_BASE}/browser/action", json=browser_action)
        result = response.json()
        
        if result["status"] == "success":
            print(f"导航成功 - 标题: {result['result']['title']}")
            print(f"当前URL: {result['result']['url']}")
        else:
            print(f"导航失败: {result['error']}")

async def terminal_api_example():
    """终端API使用示例"""
    print("\n=== 终端API示例 ===")
    
    # 创建一个终端ID
    terminal_id = "api_example"
    
    # 使用WebSocket连接到终端
    async with connect(f"ws://localhost:8330/terminal") as websocket:
        # 发送初始化消息
        await websocket.send(json.dumps({
            "type": "init",
            "terminal_id": terminal_id
        }))
        
        # 接收初始化响应
        response = json.loads(await websocket.recv())
        print(f"终端初始化: {response.get('success', False)}")
        
        # 发送命令
        await websocket.send(json.dumps({
            "type": "input",
            "content": "echo 'Hello from API'; ls -la\n"
        }))
        
        # 接收输出 (最多接收5条消息或等待5秒)
        count = 0
        try:
            while count < 5:
                response = json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))
                print(f"终端输出: {response.get('content', '')}")
                count += 1
        except asyncio.TimeoutError:
            print("终端输出接收超时")
    
    # 使用HTTP API获取终端历史
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/terminal/{terminal_id}/view?full=true")
        result = response.json()
        
        if result["status"] == "success":
            print(f"\n获取终端历史成功, 共 {len(result['output'])} 行")
        else:
            print(f"获取终端历史失败: {result.get('error', 'unknown error')}")
        
        # 重置终端
        response = await client.post(f"{API_BASE}/terminal/{terminal_id}/reset")
        result = response.json()
        print(f"终端重置: {'成功' if result['status'] == 'success' else '失败'}")

async def text_editor_api_example():
    """文本编辑器API使用示例"""
    print("\n=== 文本编辑器API示例 ===")
    
    async with httpx.AsyncClient() as client:
        # 创建测试文件
        test_file = "/tmp/orion_api_test.txt"
        
        # 写入文件
        action = {
            "action": "write_file",
            "target_file": test_file,
            "content": "这是通过API创建的测试文件\n第二行内容\n第三行内容"
        }
        
        response = await client.post(f"{API_BASE}/text_editor", json=action)
        result = response.json()
        print(f"文件写入: {'成功' if result['status'] == 'success' else '失败'}")
        
        # 读取文件
        action = {
            "action": "read_file",
            "target_file": test_file
        }
        
        response = await client.post(f"{API_BASE}/text_editor", json=action)
        result = response.json()
        
        if result["status"] == "success":
            print(f"文件内容:\n{result['result']}")
        else:
            print(f"读取文件失败: {result.get('error', 'unknown error')}")
        
        # 删除文件
        action = {
            "action": "delete_file",
            "target_file": test_file
        }
        
        response = await client.post(f"{API_BASE}/text_editor", json=action)
        result = response.json()
        print(f"删除文件: {'成功' if result['status'] == 'success' else '失败'}")

async def main():
    """运行所有API示例"""
    print("Orion API调用示例\n")
    print("注意: 请确保Orion服务已在localhost:8330上运行\n")
    
    try:
        # 运行浏览器API示例
        await browser_api_example()
        
        # 运行终端API示例
        await terminal_api_example()
        
        # 运行文本编辑器API示例
        await text_editor_api_example()
    except httpx.ConnectError:
        print("\n错误: 无法连接到Orion服务器。请确保服务器正在运行。")
    except Exception as e:
        print(f"\n错误: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 