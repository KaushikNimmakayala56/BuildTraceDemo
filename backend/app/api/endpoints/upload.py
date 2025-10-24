"""
File upload endpoint
"""
from fastapi import APIRouter, File, UploadFile
from app.models.schemas import FileUploadResponse, ErrorResponse
from app.services.file_service import FileService

router = APIRouter()
file_service = FileService()


@router.post(
    "/upload",
    response_model=FileUploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Invalid file type"},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity - Cannot extract text"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Upload and process file",
    description="Upload a PDF or image file to extract text content using OCR"
)
async def upload_file(file: UploadFile = File(..., description="PDF or image file to process")):
    """
    Upload and process a file to extract text
    
    - **file**: PDF or image file (jpg, png, gif, bmp, tiff)
    
    Returns extracted text along with file metadata
    """
    result = await file_service.process_file(file)
    return result

