from typing import Any, List
import bashlex
import bashlex.errors
from app.logger import logger

__all__ = [
    'process_terminal_output',
    'split_bash_commands'
]

def split_bash_commands(commands):
    """
    能够将类似 'ls -l \n echo hello' 这样的命令拆分成两个单独的命令 
    但是类似 'echo a && echo b' 这样的命令不会被拆分 
    Copy from OpenHands:
    https://github.com/All-Hands-AI/OpenHands/blob/main/openhands/runtime/utils/bash.py
    """
    if not commands.strip():
        return ['']
    
    try:
        parsed = bashlex.parse(commands)
        result = []
        start = 0
        
        for node in parsed:
            if hasattr(node, 'pos') and hasattr(node, 'end'):
                cmd = commands[node.pos:node.end].strip()
                result.append(cmd)
        
        if not result and commands.strip():
            if '\n' in commands:
                return [cmd.strip() for cmd in commands.split('\n') if cmd.strip()]
            else:
                return [commands.strip()]
        
        return result
    except (bashlex.errors.ParsingError, Exception) as e:
        if '\n' in commands:
            return [cmd.strip() for cmd in commands.split('\n') if cmd.strip()]
        return [commands.strip()] if commands.strip() else ['']

def process_terminal_output(text):
    '''
    处理终端输出，保留 ANSI 转义序列并正确处理行覆盖
    处理规则：
    1. 保留所有 ANSI 转义序列（\x1b[...m 颜色，\x1b[...G 光标移动等）
    2. 处理 \r 的行内覆盖效果
    3. 处理光标控制序列的行内覆盖效果
    '''
    if not text:
        return ""
    
    lines = text.split('\n')
    result = []
    
    for line in lines:
        if '\r' in line:
            parts = line.split('\r')
            processed_line = parts[0]
            
            for i in range(len(parts) - 1):
                ansi_colors = extract_ansi_colors(parts[i])
                if ansi_colors and not have_matching_ansi_reset(parts[0]):
                    processed_line = ansi_colors + processed_line
            
            result.append(processed_line)
        else:
            processed_line = process_cursor_movements(line)
            result.append(processed_line)
    
    return '\n'.join(result)

def extract_ansi_colors(text):
    """
    Extract ANSI color sequences from a text.
    
    Args:
        text: The text to extract colors from
        
    Returns:
        str: Concatenated color sequences found in the text
    """
    import re
    
    color_pattern = r'\x1b\[\d+(;\d+)*m'
    colors = re.findall(color_pattern, text)
    
    return ''.join(colors)

def have_matching_ansi_reset(text):
    """
    Check if the text has a matching ANSI reset sequence.
    
    Args:
        text: The text to check
        
    Returns:
        bool: True if there's a reset sequence, False otherwise
    """
    return '\x1b[0m' in text or '\x1b[m' in text

def process_cursor_movements(line):
    """
    Process cursor movement escape sequences.
    
    Args:
        line: Line to process
        
    Returns:
        str: Processed line with cursor movements applied
    """
    import re
    
    cursor_pattern = r'\x1b\[(\d+)G'
    matches = list(re.finditer(cursor_pattern, line))
    
    if not matches:
        return line
    
    result = list(line)
    for match in reversed(matches):
        col = int(match.group(1)) - 1
        cmd_start = match.start()
        cmd_end = match.end()
        
        for i in range(cmd_start, cmd_end):
            result[i] = ''
    
    return ''.join(result)