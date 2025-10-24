"""
Main file processing service that orchestrates PDF and image processing
"""
import mimetypes
from fastapi import HTTPException, UploadFile
from app.services.pdf_processor import PDFProcessor
from app.services.image_processor import ImageProcessor


class FileService:
    """Service for handling file uploads and processing"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.image_processor = ImageProcessor()
    
    async def process_file(self, file: UploadFile) -> dict:
        """
        Process uploaded file and extract text
        
        Args:
            file: Uploaded file from FastAPI
            
        Returns:
            Dictionary containing extracted text, filename, and file type
            
        Raises:
            HTTPException: If file type is unsupported or processing fails
        """
        # Read file content
        file_content = await file.read()
        
        # Detect file type
        file_type = mimetypes.guess_type(file.filename)[0]
        
        if not file_type:
            raise HTTPException(
                status_code=400,
                detail="Could not determine file type. Please ensure the file has a proper extension."
            )
        
        # Process based on file type
        extracted_text = ""
        
        if file_type == "application/pdf":
            extracted_text = self.pdf_processor.extract_text(file_content)
            
        elif file_type.startswith("image/"):
            extracted_text = self.image_processor.extract_text(file_content)
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_type}. Please upload PDF or image files."
            )
        
        return {
            "text": extracted_text,
            "filename": file.filename,
            "file_type": file_type
        }

