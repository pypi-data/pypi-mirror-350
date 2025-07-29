import asyncio
import os
import aiohttp
from app.logger import logger
from functools import wraps
from pathlib import Path
from typing import List
from fastapi import HTTPException
from app.models import DownloadResult, PartUploadResult, PresignedUrlPart
from app.tools.base import DEFAULT_WORKING_DIR


async def upload_to_presigned_url(data, presigned_url):
    '''
    Upload data to a presigned URL.
    
    Args:
        data: The data to upload (bytes or file-like object)
        presigned_url: The presigned URL to upload to
    
    Returns:
        dict: Response data from the upload
    '''
    
    async with aiohttp.ClientSession(skip_auto_headers=['Content-Type']) as session:
        try:
            async with session.put(presigned_url, data=data) as response:
                if 200 <= response.status < 300:
                    return {'success': True}
                else:
                    error_text = await response.text()
                    return {'success': False, 'error': error_text}
        except Exception as e:
            return {'success': False, 'error': str(e)}

async def upload_part(session, url, data, part_number):
    '''Upload a single part to presigned URL'''
    try:
        async with session.put(url, data=data) as response:
            if 200 <= response.status < 300:
                etag = response.headers.get('ETag', '').strip('"')
                return PartUploadResult(
                    part_number=part_number,
                    success=True,
                    etag=etag
                )
            else:
                error_text = await response.text()
                return PartUploadResult(
                    part_number=part_number,
                    success=False,
                    error=error_text
                )
    except Exception as e:
        return PartUploadResult(
            part_number=part_number,
            success=False,
            error=str(e)
        )

class FilePartReader:
    '''
    A context manager for reading parts of a file
    '''
    def __init__(self, file_path, part_size):
        self.file_path = file_path
        self.part_size = part_size
        self._file = None
    
    async def __aenter__(self):
        self._file = open(self.file_path, 'rb')
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()
    
    def read_part(self, part_number):
        '''读取指定分片的数据'''
        offset = (part_number - 1) * self.part_size
        self._file.seek(offset)
        return self._file.read(self.part_size)

async def upload_parts_to_presigned_url(file_path, presigned_urls: List[PresignedUrlPart], part_size, max_concurrent = 2) -> List[PartUploadResult]:
    '''
    并发上传文件分片 (Concurrently upload file parts)
    
    Args:
        file_path: 文件路径
        presigned_urls: 预签名URL列表
        part_size: 分片大小（字节）
        max_concurrent: 最大并发数
    
    Returns:
        List[PartUploadResult]: Results of all part uploads
    '''
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not presigned_urls:
        raise ValueError("No presigned URLs provided")
    
    sorted_urls = sorted(presigned_urls, key=lambda x: x.part_number)
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def upload_part_with_semaphore(session, url_obj: PresignedUrlPart):
        async with semaphore:
            try:
                part_number = url_obj.part_number
                url = url_obj.url
                async with FilePartReader(file_path, part_size) as reader:
                    data = reader.read_part(part_number)
                    result = await upload_part(session, url, data, part_number)
                    return result
            except Exception as e:
                logger.error(f"Error uploading part {url_obj.part_number}: {e}")
                return PartUploadResult(
                    part_number=url_obj.part_number,
                    success=False,
                    error=str(e)
                )
    
    async with aiohttp.ClientSession(skip_auto_headers=['Content-Type']) as session:
        tasks = [upload_part_with_semaphore(session, url_obj) for url_obj in sorted_urls]
        results = await asyncio.gather(*tasks)
        success_count = sum(1 for r in results if r.success)
        logger.info(f"Multipart upload completed: {success_count}/{len(results)} parts successful")
        return results

async def download_file(session, folder_path, item):
    file_name = os.path.basename(item.filename)
    base_path = Path(DEFAULT_WORKING_DIR) / 'download'
    target_path = base_path
    
    if folder_path:
        subfolder = folder_path.strip('/')
        target_path = os.path.join(base_path, subfolder)
    
    os.makedirs(target_path, exist_ok=True)
    file_path = os.path.join(target_path, file_name)
    
    try:
        response = await session.get(item.url)
        if response.status != 200:
            error_text = await response.text()
            return DownloadResult(
                filename=file_name,
                file_path=file_path,
                success=False,
                error=error_text
            )
        
        with open(file_path, 'wb') as f:
            async for chunk in response.content.iter_chunked(8192):
                f.write(chunk)
        
        return DownloadResult(
            filename=file_name,
            file_path=file_path,
            success=True
        )
    except Exception as e:
        logger.error(f"Error downloading file {file_name}: {str(e)}")
        return DownloadResult(
            filename=file_name,
            file_path=file_path,
            success=False,
            error=str(e)
        )

def handle_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper