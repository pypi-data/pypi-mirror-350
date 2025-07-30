from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel
from functools import wraps

from app.helpers.tool_helpers import MAX_RESPONSE_LEN, TRUNCATED_MESSAGE, maybe_truncate, run_shell
from app.types.messages import FileInfo, TextEditorActionResult
from app.types.messages import TextEditorCommand as Command
from app.tools.base import DEFAULT_WORKING_DIR
from app.logger import logger

class ToolResult(BaseModel):
    output: str
    file_info: FileInfo | None = None

class ToolError(Exception):
    """Raised when a tool encounters an error."""
    def __init__(self, message: str):
        self.message = message

def validate_path(command: Command, path: Path) -> Path:
    '''
    Check that the path/command combination is valid.
    
    Args:
        command: The command being performed
        path: The path to validate
    
    Returns:
        Path: The validated path
    
    Raises:
        ToolError: If the path is invalid for the given command
    '''
    if path.is_absolute() and DEFAULT_WORKING_DIR:
        path = Path(DEFAULT_WORKING_DIR) / path.relative_to('/')
    
    if not path.is_absolute() and DEFAULT_WORKING_DIR:
        path = Path(DEFAULT_WORKING_DIR) / path
    
    if not path.exists() and command not in ('create', 'write', 'move_new'):
        raise ToolError(f'The path {path} does not exist. Please provide a valid path.')
    
    if path.exists():
        if command == 'create':
            if path.is_file() or path.stat().st_size > 0:
                raise ToolError(f'Non-empty file already exists at: {path}. Cannot overwrite non-empty files using command `create`.')
        elif command in ('dir', 'find_file'):
            if not path.is_dir():
                raise ToolError(f'The path {path} is not a directory.')
        elif command in ('move', 'delete'):
            pass
        elif path.is_dir():
            raise ToolError(f'The path {path} is a directory. Directory operations are not supported for this command.')
    
    return path

def _make_output(file_content: str, file_descriptor: str, init_line: int = 1, expand_tabs: bool = True) -> str:
    '''
    Format file content for output with line numbers.
    
    Args:
        file_content: The content to format
        file_descriptor: Description of the file (usually path)
        init_line: Initial line number
        expand_tabs: Whether to expand tabs to spaces
    
    Returns:
        str: Formatted output with line numbers
    '''
    if expand_tabs:
        file_content = file_content.expandtabs(4)
    
    header = f"Here's the result of running `cat -n` on {file_descriptor}:\n"
    line_width = 8  # Width for line numbers
    max_content_length = MAX_RESPONSE_LEN - len(header) - len(TRUNCATED_MESSAGE)
    lines = file_content.split('\n')
    line_num_chars = line_width * len(lines)
    max_content_length -= line_num_chars
    
    if len(file_content) > max_content_length:
        content_parts = []
        current_length = 0
        
        for i, line in enumerate(lines):
            if current_length + len(line) + 1 > max_content_length:
                break
            
            content_parts.append(line)
            current_length += len(line) + 1
        
        file_content = '\n'.join(content_parts)
        file_content = maybe_truncate(file_content, max_content_length)
    
    numbered_lines = []
    for i, line in enumerate(file_content.split('\n')):
        line_num = i + init_line
        numbered_lines.append(f"{line_num:>{line_width-1}}  {line}")
    
    return header + '\n'.join(numbered_lines)

async def dir(path: Path) -> ToolResult:
    '''
    List contents of a directory.
    
    Args:
        path: Directory path to list
    
    Returns:
        ToolResult: The directory listing
    '''
    path = validate_path('dir', Path(path))
    
    cmd = f'ls -la "{path}"'
    return_code, stdout, stderr = await run_shell(cmd)
    
    if return_code != 0:
        raise ToolError(f"Failed to list directory {path}: {stderr}")

    return ToolResult(output=f"Directory contents of {path}:\n\n{stdout}")

async def view(path: Path, view_range: Optional[List[int]], sudo: bool) -> ToolResult:
    '''
    View the content of a file.
    
    Args:
        path: File path to view
        view_range: Optional line range to view [start, end]
        sudo: Whether to use sudo privileges
    
    Returns:
        ToolResult: The file content
    '''
    path = validate_path('view', Path(path))
    
    file_content = await read_file(path, sudo)
    if view_range and len(view_range) == 2:
        start, end = view_range
        lines = file_content.split('\n')
        start = max(1, min(start, len(lines))) - 1
        end = max(start + 1, min(end, len(lines)))
        file_content = '\n'.join(lines[start:end])
    
    output = _make_output(file_content, str(path), 1, True)
    file_info = FileInfo(path=str(path), content=file_content)
    return ToolResult(output=output, file_info=file_info)

async def create(path: Path, file_text: str, sudo: bool) -> ToolResult:
    '''
    Create a new file with the given content.
    
    Args:
        path: File path to create   
        file_text: Content to write to the file
        sudo: Whether to use sudo privileges
    
    Returns:
        ToolResult: The result of the operation
    '''
    path = validate_path('create', Path(path))
    return await write_file(path, file_text, sudo, False, False, False)

async def write(path: Path, file_text: str, sudo: bool, append: bool, trailing_newline: bool, leading_newline: bool) -> ToolResult:
    '''
    Write content to a file.
    
    Args:
        path: File path to write to 
        file_text: Content to write to the file
        sudo: Whether to use sudo privileges
        append: If True, append content to file instead of overwriting
        trailing_newline: If True, add a newline at the end of content
        leading_newline: If True, add a newline at the beginning of content
    
    Returns:
        ToolResult: The result of the operation
    '''
    path = validate_path('write', Path(path))
    return await write_file(path, file_text, sudo, append, trailing_newline, leading_newline)

async def replace(path: Path, old_str: str, new_str: str, sudo: bool) -> ToolResult:
    '''
    Replace occurrences of old_str with new_str in the file.
    
    Args:
        path: File path to modify
        old_str: String to replace
        new_str: Replacement string
        sudo: Whether to use sudo privileges
    
    Returns:
        ToolResult: The result of the operation
    '''
    path = validate_path('replace', Path(path))
    
    if not old_str:
        raise ToolError("old_str cannot be empty")
    
    old_content = await read_file(path, sudo)
    if old_str not in old_content:
        return ToolResult(
            output=f"Warning: The string '{old_str}' was not found in {path}.",
            file_info=FileInfo(path=str(path), content=old_content)
        )
    
    new_content = old_content.replace(old_str, new_str)
    await write_file(path, new_content, sudo, False, False, False)
    replacements = old_content.count(old_str)
    return ToolResult(
        output=f"Successfully replaced {replacements} occurrence(s) of '{old_str}' with '{new_str}' in {path}.",
        file_info=FileInfo(path=str(path), content=new_content, old_content=old_content)
    )

async def find_content(path: Path, regex: str, sudo: bool) -> ToolResult:
    '''
    Find content matching regex in the file.
    
    Args:
        path: File path to search
        regex: Regular expression pattern to search for
        sudo: Whether to use sudo privileges
    
    Returns:
        ToolResult: The search results
    '''
    path = validate_path('find_content', Path(path))

    if not regex:
        raise ToolError("regex pattern cannot be empty")
    
    grep_cmd = f"{'sudo ' if sudo else ''}grep -n '{regex}' '{path}'"
    return_code, stdout, stderr = await run_shell(grep_cmd)
    file_content = await read_file(path, sudo)
    
    if return_code != 0 and not stderr:
        return ToolResult(
            output=f"No matches found for pattern '{regex}' in {path}.",
            file_info=FileInfo(path=str(path), content=file_content)
        )
    elif return_code != 0:
        raise ToolError(f"Error searching file: {stderr}")
    
    results = [f"Line {match.split(':', 1)[0]}: {match.split(':', 1)[1]}" for match in stdout.strip().split('\n') if match]
    output = f"Found {len(results)} matches for pattern '{regex}' in {path}:\n\n" + '\n'.join(results)
    return ToolResult(
        output=output,
        file_info=FileInfo(path=str(path), content=file_content)
    )

async def find_file(path: Path, glob_pattern: str) -> ToolResult:
    '''
    Find files matching glob pattern in directory.
    
    Args:
        path: Directory path to search
        glob_pattern: Glob pattern to match files
        
    Returns:
        ToolResult: The search results
    '''
    path = validate_path('find_file', Path(path))
    
    if not glob_pattern:
        glob_pattern = "*"
    
    find_cmd = f"find '{path}' -type f -name '{glob_pattern}' | sort"
    return_code, stdout, stderr = await run_shell(find_cmd)
    
    if return_code != 0:
        raise ToolError(f"Error finding files: {stderr}")
    
    files = stdout.strip().split('\n')
    if not files or (len(files) == 1 and not files[0]):
        return ToolResult(output=f"No files matching pattern '{glob_pattern}' found in {path}.")
    
    output = f"Found {len(files)} files matching pattern '{glob_pattern}' in {path}:\n\n" + '\n'.join(files)
    return ToolResult(output=output)

async def read_file(path: Path, sudo: bool) -> str:
    '''
    Read the content of a file from a given path.
    
    Args:
        path: File path to read
        sudo: Whether to use sudo privileges
        
    Returns:
        str: The file content
        
    Raises:
        ToolError: If an error occurs while reading the file
    '''
    if not path.exists():
        raise ToolError(f"File does not exist: {path}")
    
    if path.is_dir():
        raise ToolError(f"Cannot read directory as file: {path}")
    
    cat_cmd = f"{'sudo ' if sudo else ''}cat '{path}'"
    return_code, stdout, stderr = await run_shell(cat_cmd)
    
    if return_code != 0:
        raise ToolError(f"Failed to read file {path}: {stderr}")
    
    return stdout

async def write_file(path: Path, content: str, sudo: bool, append: bool, trailing_newline: bool, leading_newline: bool) -> ToolResult:
    """
    Write content to a file.
    
    Args:
        path: File path to write to
        content: Content to write
        sudo: Whether to use sudo privileges
        append: If True, append content to file instead of overwriting
        trailing_newline: If True, add a newline at the end of content
        leading_newline: If True, add a newline at the beginning of content
    
    Returns:
        ToolResult: The result of the operation
    
    Raises:
        ToolError: If an error occurs while writing the file
    """
    if not path.parent.exists():
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ToolError(f"Failed to create directory {path.parent}: {str(e)}")
    
    if leading_newline and not content.startswith('\n'):
        content = '\n' + content
    
    if trailing_newline and not content.endswith('\n'):
        content = content + '\n'
    
    old_content = ""
    if path.exists() and path.is_file() and append:
        old_content = await read_file(path, sudo)
        content = old_content + content
    
    temp_path = path.with_name(f".tmp_{path.name}")
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if sudo:
        mv_cmd = f"sudo mv '{temp_path}' '{path}'"
        return_code, stdout, stderr = await run_shell(mv_cmd)
        
        if return_code != 0:
            raise ToolError(f"Failed to write file {path}: {stderr}")
    else:
        try:
            temp_path.replace(path)
        except Exception as e:
            raise ToolError(f"Failed to write file {path}: {str(e)}")
    
    action = "Created" if not append or not path.exists() else "Updated"
    
    return ToolResult(
        output=f"{action} file {path} successfully.",
        file_info=FileInfo(path=str(path), content=content, old_content=old_content if append else None)
    )

async def move(path: Path, new_path: Path, sudo: bool) -> ToolResult:
    '''
    Move a file or directory to a new location.
    
    Args:
        path: Source path to move
        new_path: Destination path
        sudo: Whether to use sudo privileges
    
    Returns:
        ToolResult: The result of the operation
    '''
    path = validate_path('move', Path(path))
    new_path = validate_path('move_new', Path(new_path))
    
    if not path.exists():
        raise ToolError(f"Source path {path} does not exist")
    
    if new_path.exists():
        raise ToolError(f"Destination path {new_path} already exists")
    
    if not new_path.parent.exists():
        try:
            new_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ToolError(f"Failed to create directory {new_path.parent}: {str(e)}")
    
    mv_cmd = f"{'sudo ' if sudo else ''}mv '{path}' '{new_path}'"
    return_code, stdout, stderr = await run_shell(mv_cmd)
    
    if return_code != 0:
        raise ToolError(f"Failed to move {path} to {new_path}: {stderr}")
    
    return ToolResult(output=f"Successfully moved {path} to {new_path}")

async def delete(path: Path, sudo: bool) -> ToolResult:
    '''
    Delete a file or directory.
    
    Args:
        path: Path to delete
        sudo: Whether to use sudo privileges
    
    Returns:
        ToolResult: The result of the operation
    '''
    path = validate_path('delete', Path(path))
    
    if not path.exists():
        raise ToolError(f"Path {path} does not exist")
    
    rm_cmd = f"{'sudo ' if sudo else ''}rm -rf '{path}'"
    return_code, stdout, stderr = await run_shell(rm_cmd)
    
    if return_code != 0:
        raise ToolError(f"Failed to delete {path}: {stderr}")
    
    return ToolResult(output=f"Successfully deleted {path}")

def handle_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            assert result.output, "text editor action must has an output"
            return TextEditorActionResult(
                status="success",
                result=result.output,
                file_info=result.file_info
            )
        except ToolError as e:
            logger.error(f"Error: {e}")
            return TextEditorActionResult(
                status="error",
                result=e.message,
                file_info=None
            )
        except Exception as e:
            logger.error(f"Error: {e}")
            return TextEditorActionResult(
                status="error",
                result=str(e),
                file_info=None
            )
    return wrapper