"""
Application configuration settings
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "Smart Text Extractor API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Extract text from PDFs and images using OCR"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:80",
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
    
    class Config:
        case_sensitive = True


settings = Settings()

