"""
Health check endpoint
"""
from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    summary="Health check",
    description="Check if the API is running"
)
async def health_check():
    """
    Health check endpoint
    
    Returns a simple message indicating the API is running
    """
    return {
        "message": "Smart Text Extractor API is running",
        "status": "healthy"
    }


@router.get(
    "/health",
    summary="Detailed health check",
    description="Get detailed health status of the API"
)
async def detailed_health_check():
    """
    Detailed health check endpoint
    
    Returns detailed information about API health
    """
    return {
        "status": "healthy",
        "api": "Smart Text Extractor",
        "version": "1.0.0",
        "services": {
            "pdf_processor": "operational",
            "image_processor": "operational"
        }
    }

