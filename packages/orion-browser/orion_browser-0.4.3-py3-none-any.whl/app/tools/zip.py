import os
import shutil
import tempfile
from functools import wraps
from fastapi import HTTPException

def zip_dir(source_dir: str, output_zip: str) -> tuple[bool, str]:
    '''
    Zip a directory, excluding node_modules and .next

    Args:
        source_dir: Path to the directory to zip
        output_zip: Path for the output zip file

    Returns:
        tuple[bool, str]: (success, error_message)
    '''
    try:
        if not os.path.isdir(source_dir):
            return {
                'success': False,
                'error': f"Directory '{source_dir}' does not exist"
            }
        
        if not output_zip.endswith('.zip'):
            output_zip += '.zip'
        
        exclude_patterns = [
            'node_modules',
            '.next',
            '.open-next',
            '.turbo',
            '.git',
            '.vnc'
        ]
        
        def copy_files(src, dst, ignores=exclude_patterns):
            for item in os.listdir(src):
                if item in ignores:
                    continue
                    
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                
                if os.path.isdir(s):
                    shutil.copytree(s, d, ignore=lambda x, y: ignores)
                else:
                    shutil.copy2(s, d)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            source_copy = os.path.join(temp_dir, 'source')
            os.makedirs(source_copy)
            copy_files(str(source_dir), source_copy)
            shutil.make_archive(output_zip[:-4], 'zip', source_copy)
        
        return {
            'success': True,
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Failed to create zip archive: {str(e)}"
        }

def handle_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper