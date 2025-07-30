from typing import Literal
from pydantic import BaseModel
from app.types.browser_types import BrowserAction, BrowserActionResult

TextEditorCommand = Literal['dir', 'view', 'create', 'write', 'replace', 'find_content', 'find_file', 'move', 'delete']

class CommonApiResult(BaseModel):
    status: Literal['success', 'error']
    error: str | None = None

class FileActionResult(BaseModel):
    status: Literal['success', 'error']
    result: str

class TextEditorDirRequest(BaseModel):
    path: str
    sudo: bool | None = None

class TextEditorViewRequest(BaseModel):
    path: str
    sudo: bool | None = None
    view_range: list[int] | None = None

class TextEditorCreateRequest(BaseModel):
    path: str
    sudo: bool | None = None
    file_text: str

class TextEditorWriteRequest(BaseModel):
    path: str
    sudo: bool | None = None
    file_text: str
    append: bool | None = None
    leading_newline: bool | None = None
    trailing_newline: bool | None = None

class TextEditorStrReplaceRequest(BaseModel):
    path: str
    sudo: bool | None = None
    old_str: str
    new_str: str

class TextEditorFindContentRequest(BaseModel):
    path: str
    sudo: bool | None = None
    regex: str

class TextEditorFindFileRequest(BaseModel):
    path: str
    sudo: bool | None = None
    glob: str

class TextEditorMoveRequest(BaseModel):
    path: str
    sudo: bool | None = None
    new_path: str

class TextEditorDeleteRequest(BaseModel):
    path: str
    sudo: bool | None = None

class FileInfo(BaseModel):
    path: str
    content: str
    old_content: str | None = None

class TextEditorActionResult(CommonApiResult):
    result: str
    file_info: FileInfo | None = None

class BrowserActionRequest(BaseModel):
    action: BrowserAction
    screenshot_presigned_url: str | None = None
    clean_screenshot_presigned_url: str | None = None

class BrowserActionResponse(CommonApiResult):
    result: BrowserActionResult | None = None

class TerminalWriteApiRequest(BaseModel):
    text: str
    enter: bool | None = None

class TerminalApiResponse(CommonApiResult):
    output: list[str]
    result: str
    terminal_id: str

TerminalInputMessageType = Literal['command', 'view', 'view_last', 'kill', 'reset', 'reset_all']
TerminalOutputMessageType = Literal['update', 'finish', 'partial_finish', 'error', 'history', 'action_finish']
TerminalCommandMode = Literal['run', 'send_line', 'send_key', 'send_control']
TerminalStatus = Literal['idle', 'running']

class TerminalInputMessage(BaseModel):
    type: TerminalInputMessageType
    terminal: str
    action_id: str
    command: str | None = None
    mode: TerminalCommandMode | None = None
    exec_dir: str | None = None

    def create_response(self, type: TerminalOutputMessageType, result: str, output: list[str], terminal_status: TerminalStatus, sub_command_index: int = 0):
        return TerminalOutputMessage(
            type=type,
            terminal=self.terminal,
            action_id=self.action_id,
            sub_command_index=sub_command_index,
            result=result,
            output=output,
            terminal_status=terminal_status
        )

class TerminalOutputMessage(BaseModel):
    type: TerminalOutputMessageType
    terminal: str
    action_id: str
    sub_command_index: int = 0 
    result: str | None = None
    output: list[str]
    terminal_status: Literal['idle', 'running', 'unknown']
