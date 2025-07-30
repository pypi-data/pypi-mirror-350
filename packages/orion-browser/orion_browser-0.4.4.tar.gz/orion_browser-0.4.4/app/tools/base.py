import os
from pathlib import Path

# Default working directory inside the container
wd = os.getenv('WORKDIR') or '/home/ubuntu/workspace'
# Check if running inside a container by verifying if the default working directory exists
IS_INSIDE_CONTAINER = os.path.exists(wd)
# Determine the default working directory based on environment
DEFAULT_WORKING_DIR = wd if IS_INSIDE_CONTAINER else os.path.normpath(os.path.join(__file__, '../../../'))
# Determine the default user based on environment
DEFAULT_USER = 'ubuntu' if IS_INSIDE_CONTAINER else os.environ.get('USER')

def get_file_path(path: str) -> Path:
    file_path = Path(path)
    if file_path.is_absolute() and DEFAULT_WORKING_DIR:
        file_path = Path(DEFAULT_WORKING_DIR) / file_path.relative_to('/')

    if not file_path.is_absolute() and DEFAULT_WORKING_DIR:
        file_path = Path(DEFAULT_WORKING_DIR) / file_path

    return file_path

def validate_file_path(file_path: str) -> Path:
    if not file_path.exists():
        raise Exception(f"File not found: {file_path}")
    if not file_path.is_file():
        raise Exception(f"Path is not a file: {file_path}")
    return file_path

def validate_dir_path(dir_path: str) -> Path:
    if not dir_path.exists():
        raise Exception(f"Directory not found: {dir_path}")
    if not dir_path.is_dir():
        raise Exception(f"Path is not a directory: {dir_path}")
    return dir_path