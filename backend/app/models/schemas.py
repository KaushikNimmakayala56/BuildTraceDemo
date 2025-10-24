"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    """Response model for file upload"""
    text: str
    filename: str
    file_type: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Extracted text content...",
                "filename": "document.pdf",
                "file_type": "application/pdf"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Error message description"
            }
        }

