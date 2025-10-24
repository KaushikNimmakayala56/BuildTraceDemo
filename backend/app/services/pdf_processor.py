"""
PDF processing service
"""
import io
import PyPDF2
from fastapi import HTTPException


class PDFProcessor:
    """Service for processing PDF files"""
    
    @staticmethod
    def extract_text(file_content: bytes) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_content: Binary content of the PDF file
            
        Returns:
            Extracted text as string
            
        Raises:
            HTTPException: If PDF processing fails
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            extracted_text = ""
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
            
            if not extracted_text.strip():
                raise HTTPException(
                    status_code=422,
                    detail="No text could be extracted from the PDF. The file might be image-based or empty."
                )
            
            return extracted_text.strip()
            
        except PyPDF2.errors.PdfReadError as e:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid or corrupted PDF file: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing PDF: {str(e)}"
            )

