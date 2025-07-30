from pydantic import BaseModel
from typing import List, Optional, Dict

class PresignedUrlPart(BaseModel):
    part_number: int
    url: str

class FileUploadRequest(BaseModel):
    file_path: str
    presigned_url: str
    
class MultipartUploadRequest(BaseModel):
    file_path: str
    presigned_urls: List[PresignedUrlPart]
    part_size: int
    max_concurrent: Optional[int] = 2

class ZipAndUploadRequest(BaseModel):
    directory: str
    presigned_url: str

class PartUploadResult(BaseModel):
    part_number: int
    etag: Optional[str] = ""
    success: bool
    error: Optional[str] = None

class MultipartUploadResponse(BaseModel):
    status: str
    message: str
    file_name: str
    parts_results: List[PartUploadResult]
    successful_parts: List[int]
    failed_parts: List[int]

class ZipAndUploadResponse(BaseModel):
    status: str
    message: str
    error: str | None = None

class DownloadItem(BaseModel):
    url: str
    filename: str

class DownloadRequest(BaseModel):
    files: List[DownloadItem]
    folder_path: str | None = None

class DownloadResult(BaseModel):
    filename: str
    file_path: str
    success: bool
    error: str | None = None