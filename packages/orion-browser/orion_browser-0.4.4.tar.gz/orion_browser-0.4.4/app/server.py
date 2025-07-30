import asyncio
import math
import mimetypes
import os
import time
from typing import Dict
import aiohttp
import httpx
from fastapi import Body, FastAPI, HTTPException, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.logger import logger
from app.models import DownloadRequest, FileUploadRequest, MultipartUploadRequest, MultipartUploadResponse, ZipAndUploadRequest, ZipAndUploadResponse
from app.router import TimedRoute
from app.tools.terminal.terminal_socket import terminal_socket
from app.tools.terminal.terminal_manager import terminal_manager
from app.tools.base import get_file_path, validate_dir_path, validate_file_path
from app.tools.browser.browser_manager import BrowserDeadError, BrowserManager, PageDeadError
from app.types.messages import BrowserActionRequest, BrowserActionResponse, TerminalApiResponse, TerminalWriteApiRequest, TextEditorCreateRequest, TextEditorDeleteRequest, TextEditorDirRequest, TextEditorFindContentRequest, TextEditorFindFileRequest, TextEditorMoveRequest, TextEditorStrReplaceRequest, TextEditorViewRequest, TextEditorWriteRequest
import app.tools.editor as editor
import app.tools.file as file
import app.tools.zip as zip

app = FastAPI()
app.router.route_class = TimedRoute
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MULTIPART_THRESHOLD = 10485760  # 10MB

@app.post("/file/upload")
@file.handle_error
async def upload_file(request: FileUploadRequest = Body(...)):
    """Upload a file to presigned_url. If file size exceeds threshold, return size information instead."""
    file_path = validate_file_path(get_file_path(request.file_path))
    file_size = file_path.stat().st_size
    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    file_name = file_path.name
    
    if file_size > MULTIPART_THRESHOLD:
        return {
            "status": "need_multipart",
            "message": "File size exceeds single upload limit",
            "file_name": file_name,
            "content_type": content_type,
            "file_size": file_size,
            "need_multipart": True,
            "recommended_part_size": MULTIPART_THRESHOLD,
            "estimated_parts": file_size // MULTIPART_THRESHOLD + 1
        }
    
    with open(file_path, 'rb') as f:
        content = f.read()
    
    upload_result = await file.upload_to_presigned_url(
        data=content,
        presigned_url=request.presigned_url
    )
    
    if not upload_result:
        raise Exception("File uploaded failed")
    
    if not upload_result['success']:
        raise Exception(f"File uploaded failed: {upload_result['error']}")
    
    return {
        "status": "success",
        "message": "File uploaded successfully",
        "file_name": file_name,
        "content_type": content_type,
        "file_size": file_size,
        "need_multipart": False,
        "upload_result": {"success": True, "uploaded": True}
    }

@app.post("/file/multipart_upload")
@file.handle_error
async def multipart_upload_file(request: MultipartUploadRequest = Body(...)):
    """Upload file chunks using presigned URLs"""
    file_path = validate_file_path(get_file_path(request.file_path))
    file_size = file_path.stat().st_size
    expected_parts = math.ceil(file_size / request.part_size)
    
    if len(request.presigned_urls) != expected_parts:
        raise Exception(f"Number of presigned URLs ({len(request.presigned_urls)}) does not match expected parts ({expected_parts})")
    
    results = await file.upload_parts_to_presigned_url(str(file_path), request.presigned_urls, request.part_size, request.max_concurrent)
    
    successful_parts = [r.part_number for r in results if r.success]
    failed_parts = [r.part_number for r in results if not r.success]
    
    response = MultipartUploadResponse(
        status="success" if not failed_parts else "partial_success",
        message="All parts uploaded successfully" if not failed_parts else f"Uploaded {len(successful_parts)}/{len(results)} parts successfully",
        file_name=file_path.name,
        parts_results=results,
        successful_parts=successful_parts,
        failed_parts=failed_parts
    )
    
    return response

@app.post("/file/download")
@file.handle_error
async def download_files(request: DownloadRequest = Body(...)):
    """Download files into vm"""
    results = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [file.download_file(session, request.folder_path, item) for item in request.files]
        results = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count
    
    return {
        "status": "completed",
        "total": len(results),
        "success_count": success_count,
        "fail_count": fail_count,
        "results": results
    }

@app.get("/file")
@file.handle_error
async def get_file(path: str):
    """Download a file from vm"""
    file_path = validate_file_path(get_file_path(path))
    
    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/octet-stream"
    )

@app.post("/dir/upload")
@zip.handle_error
async def dir_upload(request: ZipAndUploadRequest):
    """Zip a directory (excluding node_modules) and upload"""
    directory_path = validate_dir_path(get_file_path(request.directory))
    project_name = os.path.basename(directory_path)
    output_zip = f"/tmp/{project_name}.zip"
    zip_result = zip.zip_dir(directory_path, output_zip)
    
    if not zip_result['success']:
        return ZipAndUploadResponse(
            status="error",
            message="Failed to create zip file",
            error=zip_result['error']
        )
    
    if not os.path.exists(output_zip):
        return ZipAndUploadResponse(
            status="error",
            message="Zip file was not created",
            error="Zip operation failed"
        )
    
    with open(output_zip, 'rb') as f:
        content = f.read()
    
    upload_result = await file.upload_to_presigned_url(
        data=content,
        presigned_url=request.presigned_url
    )
    
    if not upload_result:
        raise Exception("Zip file uploaded failed")
    
    if not upload_result['success']:
        raise Exception(f"Zip file uploaded failed: {upload_result['error']}")
    
    os.remove(output_zip)
    
    return ZipAndUploadResponse(
        status="success",
        message=f"Successfully processed {request.directory} and uploaded to presigned_url"
    )

# Initialize browser manager
browser_manager = BrowserManager(headless=False)

@app.get("/browser/status")
async def browser_status():
    """Endpoint for browser status"""
    try:
        tabs = await browser_manager.health_check()
        return {"healthy": True, "tabs": tabs}
    except BrowserDeadError as e:
        logger.error(f"Browser Error: {e}")
        return {"healthy": False, "tabs": []}

@app.post("/browser/action")
async def browser_action(cmd: BrowserActionRequest = Body()):
    """Endpoint for browser action"""
    async def execute_with_retry():
        timeout = 60
        try:
            return await asyncio.wait_for(
                browser_manager.execute_action(cmd),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            error_msg = f"Browser action timed out after {timeout}s, new tab created and opened target:blank."
            logger.error(error_msg)
            await browser_manager.recreate_page()
            raise PageDeadError(error_msg)
    
    try:
        logger.info(f"start handling browser action {repr(cmd)}")
        result = await execute_with_retry()
        
        logger.info("\n".join([
            "Browser action result:",
            "title: " + result.title,
            "url: " + result.url,
            "result: " + result.result
        ]))
        
        return BrowserActionResponse(
            status="success",
            result=result,
            error=None
        ).model_dump()
    except PageDeadError as e:
        await browser_manager.recreate_page()
        logger.error(e)
        return BrowserActionResponse(
            status="error",
            result=None,
            error=str(e)
        ).model_dump()
    except Exception as e:
        logger.error(f"Browser Error: {e}")
        return BrowserActionResponse(
            status="error",
            result=None,
            error=str(e)
        ).model_dump()

@app.post("/text_editor/dir")
@editor.handle_error
async def text_editor_dir(cmd: TextEditorDirRequest):
    return await editor.dir(cmd.path)

@app.post("/text_editor/view")
@editor.handle_error
async def text_editor_view(cmd: TextEditorViewRequest):
    return await editor.view(cmd.path, cmd.view_range, cmd.sudo)

@app.post("/text_editor/create")
@editor.handle_error
async def text_editor_create(cmd: TextEditorCreateRequest):
    return await editor.create(cmd.path, cmd.file_text, cmd.sudo)

@app.post("/text_editor/write")
@editor.handle_error
async def text_editor_write(cmd: TextEditorWriteRequest):
    return await editor.write(cmd.path, cmd.file_text, cmd.sudo, cmd.append, cmd.trailing_newline, cmd.leading_newline)

@app.post("/text_editor/replace")
@editor.handle_error
async def text_editor_replace(cmd: TextEditorStrReplaceRequest):
    return await editor.replace(cmd.path, cmd.old_str, cmd.new_str, cmd.sudo)

@app.post("/text_editor/find_content")
@editor.handle_error
async def text_editor_find_content(cmd: TextEditorFindContentRequest):
    return await editor.find_content(cmd.path, cmd.regex, cmd.sudo)

@app.post("/text_editor/find_file")
@editor.handle_error
async def text_editor_find_file(cmd: TextEditorFindFileRequest):
    return await editor.find_file(cmd.path, cmd.glob)

@app.post("/text_editor/move")
@editor.handle_error
async def text_editor_move(cmd: TextEditorMoveRequest):
    return await editor.move(cmd.path, cmd.new_path, cmd.sudo)

@app.post("/text_editor/delete")
@editor.handle_error
async def text_editor_delete(cmd: TextEditorDeleteRequest):
    return await editor.delete(cmd.path, cmd.sudo)

@app.websocket("/terminal")
async def websocket_endpoint(ws: WebSocket):
    await terminal_socket.handle_connection(ws)

@app.post("/terminal/{terminal_id}/reset")
async def reset_terminal(terminal_id: str):
    try:
        terminal = await terminal_manager.get_terminal(terminal_id)
        await terminal.reset()
        return TerminalApiResponse(
            status="success",
            result="terminal reset success",
            terminal_id=terminal_id,
            output=[]
        )
    except Exception as e:
        logger.error(f"Error resetting terminal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/terminal/reset-all")
async def reset_all_terminals():
    try:
        for terminal in terminal_manager.terminals.values():
            await terminal.reset()
        
        return TerminalApiResponse(
            status="success",
            result="all terminals reset success",
            terminal_id="",
            output=[]
        )
    except Exception as e:
        logger.error(f"Error resetting all terminals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/terminal/{terminal_id}/view")
async def view_terminal(terminal_id: str, full: bool = Query(True)):
    try:
        terminal = await terminal_manager.get_terminal(terminal_id)
        history = terminal.get_history(True, full)
        
        return TerminalApiResponse(
            status="success",
            result="terminal view success",
            terminal_id=terminal_id,
            output=history
        )
    except Exception as e:
        logger.error(f"Error viewing terminal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/terminal/{terminal_id}/kill")
async def kill_terminal_process(terminal_id: str):
    try:
        terminal = await terminal_manager.get_terminal(terminal_id)
        await terminal.kill_process()
        
        history = terminal.get_history(True, False)
        
        return TerminalApiResponse(
            status="success",
            result="terminal process killed",
            terminal_id=terminal_id,
            output=history
        )
    except Exception as e:
        logger.error(f"Error killing terminal process: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/terminal/{terminal_id}/write")
async def write_terminal_process(terminal_id: str, cmd: TerminalWriteApiRequest):
    try:
        terminal = await terminal_manager.get_terminal(terminal_id)
        await terminal.write_to_process(cmd.text, cmd.enter if cmd.enter is not None else False)
        
        # Allow time for the process to respond
        await asyncio.sleep(1)
        
        history = terminal.get_history(True, False)
        
        return TerminalApiResponse(
            status="success",
            result="write terminal process success",
            terminal_id=terminal_id,
            output=history
        )
    except Exception as e:
        logger.error(f"Error killing terminal process: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class InitSandboxRequest(BaseModel):
    secrets: Dict[str, str]

@app.post("/init-sandbox")
async def init_sandbox(request: InitSandboxRequest):
    """初始化沙箱环境  # Initialize sandbox environment

    接收 secrets 并写入到用户的 .secrets 目录下，每个 secret 作为单独的文件  # Receive secrets and write them to the user's .secrets directory, each secret as a separate file
    - secrets 目录会在 $HOME/.secrets 下创建  # The secrets directory will be created under $HOME/.secrets
    - 每个 secret 的 key 作为文件名  # Each secret's key is used as the filename
    - 如果文件已存在且内容不同，会将原文件备份（添加时间戳后缀）  # If the file already exists with different content, the original file will be backed up (with a timestamp suffix)

    Args:
        request: InitSandboxRequest containing secrets dictionary

    Returns:
        Dict with status and processed files info

    Raises:
        HTTPException: If HOME environment variable is not set or other errors
    """
    try:
        home_dir = os.getenv('WORKDIR')
        if not home_dir:
            raise HTTPException(status_code=500, detail="HOME environment variable is not set")
            
        secrets_dir = os.path.join(home_dir, '.secrets')
        
        # Create secrets directory if it doesn't exist
        os.makedirs(secrets_dir, exist_ok=True)
        os.chmod(secrets_dir, 0o700)  # rwx------
        
        processed_files = []
        
        for key, value in request.secrets.items():
            secret_file = os.path.join(secrets_dir, key)
            
            if os.path.exists(secret_file):
                try:
                    with open(secret_file, 'r') as f:
                        current_content = f.read()
                    
                    if current_content == value:
                        processed_files.append({
                            'key': key,
                            'action': 'skipped',
                            'reason': 'content unchanged'
                        })
                        continue
                    
                    if current_content != value:
                        # Backup the existing file with timestamp
                        timestamp = time.strftime('%Y%m%d_%H%M%S')
                        backup_file = f"{secret_file}.{timestamp}"
                        os.rename(secret_file, backup_file)
                        processed_files.append({
                            'key': key,
                            'action': 'backed_up',
                            'backup_file': backup_file
                        })
                except Exception as e:
                    logger.error(f"Error reading existing secret file {key}: {e}")
                    raise HTTPException(status_code=500, detail=f"Failed to process existing secret file {key}: {str(e)}")
            
            try:
                with open(secret_file, 'w') as f:
                    f.write(value)
                
                os.chmod(secret_file, 0o600)  # rw-------
                
                processed_files.append({
                    'key': key,
                    'action': 'updated' if os.path.exists(secret_file) else 'created'
                })
            except Exception as e:
                logger.error(f"Error writing secret file {key}: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to write secret file {key}: {str(e)}")
        
        return {
            'status': 'ok',
            'secrets_dir': secrets_dir,
            'processed_files': processed_files
        }
    except Exception as e:
        logger.error(f"Error processing secrets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process secrets: {str(e)}")

@app.get("/healthz")
async def healthz():
    """Health check endpoint."""
    # If browser is set to start automatically, create the task but don't await it
    if browser_manager.status == "started":
        asyncio.create_task(browser_manager.initialize())
    
    return {"status": "ok"}