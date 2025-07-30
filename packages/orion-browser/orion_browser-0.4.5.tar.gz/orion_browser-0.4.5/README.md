# Orion Sandbox

Orion是一个提供终端模拟器和浏览器代理功能的服务器。它可以作为独立服务运行，也可以作为Python包导入使用。

```

## 使用方法

### 作为服务使用

#### 方法1: 使用命令行工具

安装后，可以直接使用命令行工具启动服务：

```bash
# 使用默认配置启动
orion-server

# 指定端口和日志级别
orion-server --port 8888 --log-level debug

# 开发模式（自动重载）
orion-server --reload
```

#### 方法2: 使用Python脚本启动

```bash
python start_server.py --port 8330
```

### 作为库导入使用

可以将Orion作为Python库导入使用，示例代码：

```python
import asyncio
from app import BrowserManager, terminal_manager, text_editor

# 初始化浏览器管理器
async def browser_example():
    browser = BrowserManager(headless=False)
    await browser.initialize()
    # 执行浏览器操作...
    await browser.close()

# 使用终端管理器
async def terminal_example():
    terminal = await terminal_manager.create_or_get_terminal("my_terminal")
    await terminal.execute_command("ls -la")
    history = terminal.get_history(True, True)
    # 处理终端输出...

# 运行示例
asyncio.run(browser_example())
```

更多示例请参考 `examples/use_as_package.py`。

## Docker部署

```bash
# 构建容器
docker build -t orion-server .

# 运行容器
docker run -p 8330:8330 orion-server
```

## API文档

启动服务后，访问 `http://localhost:8330/docs` 查看API文档。

## 许可证

MIT