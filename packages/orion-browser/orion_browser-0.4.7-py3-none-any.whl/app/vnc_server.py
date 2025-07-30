import asyncio
from pathlib import Path
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.logger import logger
from app.tools.system.system_vnc import SystemVncManager
from contextlib import asynccontextmanager
import subprocess
from pydantic import BaseModel
import aiohttp
import tempfile
import os
import base64

system_vnc_manager = SystemVncManager()

class XdotoolCommand(BaseModel):
    command: str
    value: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    system_vnc_manager.start_all()
    yield
    system_vnc_manager.cleanup()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/vnc")
async def vnc_websocket_endpoint(ws: WebSocket):
    """WebSocket endpoint for VNC connections"""
    await ws.accept()
    logger.info("New VNC WebSocket connection established")
    
    try:
        reader, writer = await asyncio.open_connection('localhost', 5900)
        
        async def forward_to_vnc():
            try:
                while True:
                    data = await ws.receive_bytes()
                    writer.write(data)
                    await writer.drain()
            except Exception as e:
                logger.error(f"Error forwarding to VNC: {e}")
                writer.close()
                await writer.wait_closed()
        
        async def forward_from_vnc():
            try:
                while True:
                    data = await reader.read(65536)  # 64KB buffer for VNC data
                    if not data:
                        break
                    await ws.send_bytes(data)
            except Exception as e:
                logger.error(f"Error forwarding from VNC: {e}")
                writer.close()
                await writer.wait_closed()
        
        to_vnc = asyncio.create_task(forward_to_vnc())
        from_vnc = asyncio.create_task(forward_from_vnc())
        
        done, pending = await asyncio.wait(
            [to_vnc, from_vnc],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        for task in pending:
            task.cancel()
        
        await asyncio.gather(*pending, return_exceptions=True)
        
    except Exception as e:
        logger.error(f"VNC WebSocket error: {e}")
    finally:
        await ws.close()
        logger.info("VNC WebSocket connection closed")

@app.post("/control")
async def xdotool_command(command: XdotoolCommand):
    """Execute xdotool command in the virtual machine"""
    try:
        logger.info(f"Executing xdotool command: {command.command} {command.value}")
        # Execute xdotool command
        process = subprocess.Popen(
            ["xdotool", command.command, command.value],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            raise HTTPException(
                status_code=400,
                detail=f"xdotool command failed: {stderr.decode()}"
            )
            
        return {"status": "success", "output": stdout.decode()}
    except Exception as e:
        logger.error(f"Error executing xdotool command: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute xdotool command: {str(e)}"
        )

@app.get("/check")
async def check():
    return {"status": "success"}

async def get_ssl() -> tuple[str | None, str | None]:
    if os.environ.get("VNC_SSL_CERT") and os.environ.get("VNC_SSL_KEY"):
        cert_file = tempfile.NamedTemporaryFile(delete=False)
        key_file = tempfile.NamedTemporaryFile(delete=False)
        cert_data = base64.b64decode(os.environ.get("VNC_SSL_CERT"))
        key_data = base64.b64decode(os.environ.get("VNC_SSL_KEY"))
        
        cert_file.write(cert_data)
        key_file.write(key_data)
        cert_file.close()
        key_file.close()
        
        return Path(cert_file.name).resolve(), Path(key_file.name).resolve()
    else:
        return Path('app/key.pem').resolve(), Path('app/cert.pem').resolve()

async def start_vnc_server(host: str = "0.0.0.0", port: int = 8081):
    """Start the VNC server"""
    import uvicorn
    
    logger.info(f"Starting VNC server on {host}:{port}")
    ssl_keyfile, ssl_certfile = await get_ssl()
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile
    )
    server = uvicorn.Server(config)
    await server.serve()