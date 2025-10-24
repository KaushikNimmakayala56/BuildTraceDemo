"""
Image processing service with OCR
"""
import io
from PIL import Image
import pytesseract
from fastapi import HTTPException


class ImageProcessor:
    """Service for processing image files with OCR"""
    
    @staticmethod
    def extract_text(file_content: bytes) -> str:
        """
        Extract text from image using OCR
        
        Args:
            file_content: Binary content of the image file
            
        Returns:
            Extracted text as string
            
        Raises:
            HTTPException: If image processing fails
        """
        try:
            image = Image.open(io.BytesIO(file_content))
            
            # Perform OCR
            extracted_text = pytesseract.image_to_string(image)
            
            if not extracted_text.strip():
                raise HTTPException(
                    status_code=422,
                    detail="No text could be extracted from the image. The image might not contain readable text."
                )
            
            return extracted_text.strip()
            
        except Image.UnidentifiedImageError:
            raise HTTPException(
                status_code=422,
                detail="Invalid or corrupted image file"
            )
        except pytesseract.TesseractError as e:
            raise HTTPException(
                status_code=500,
                detail=f"OCR processing failed: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing image: {str(e)}"
            )

