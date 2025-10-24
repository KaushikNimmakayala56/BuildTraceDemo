"""
Engineering Drawing Mentor - Main FastAPI Application
Simple, clean implementation for drawing analysis
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

# Import our services
from pdf_service import get_pdf_service
from gemini_service import get_gemini_service


# Lifespan event to load PDF at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load textbook PDF at startup"""
    print("\n🚀 Starting Engineering Drawing Mentor API...")
    
    # Load PDF
    pdf_service = get_pdf_service()
    pdf_path = os.path.join(os.path.dirname(__file__), '../TEXTBOOK.pdf')
    success = pdf_service.load_and_parse(pdf_path)
    
    if not success:
        print("⚠️  Warning: Failed to load textbook PDF")
    
    # Initialize Gemini service
    try:
        get_gemini_service()
        print("✅ All services initialized!\n")
    except Exception as e:
        print(f"⚠️  Warning: Gemini service initialization failed: {e}\n")
    
    yield
    
    # Cleanup (if needed)
    print("\n👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Engineering Drawing Mentor",
    description="AI-powered tutor for engineering drawing problems",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Engineering Drawing Mentor API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint with PDF service status"""
    pdf_service = get_pdf_service()
    status = pdf_service.get_status()
    
    return {
        "status": "healthy",
        "textbook_loaded": status["loaded"],
        "total_problems": status["total_problems"],
        "problem_numbers": status["problem_numbers"]
    }


@app.post("/api/analyze")
async def analyze_drawing(file: UploadFile = File(...)):
    """
    Analyze uploaded engineering drawing
    
    Process:
    1. Extract problem number from image
    2. Retrieve relevant textbook section
    3. Analyze with Gemini AI
    4. Return structured steps
    """
    
    # Validate file type (accept images and PDFs)
    valid_types = ['image/png', 'image/jpeg', 'image/jpg', 'application/pdf']
    if file.content_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Expected image/PDF, got {file.content_type}"
        )
    
    try:
        # Read file bytes
        image_bytes = await file.read()
        print(f"\n📤 Received file: {file.filename} ({len(image_bytes)} bytes)")
        
        # Get services
        pdf_service = get_pdf_service()
        gemini_service = get_gemini_service()
        
        # Check if textbook is loaded
        if not pdf_service.loaded:
            raise HTTPException(
                status_code=503,
                detail="Textbook not loaded. Please contact administrator."
            )
        
        # Step 1: Extract problem number from image
        print("📋 Step 1: Extracting problem number...")
        problem_number = gemini_service.extract_problem_number(image_bytes)
        
        # Step 2: Retrieve relevant textbook section
        print("📖 Step 2: Retrieving textbook section...")
        if problem_number:
            textbook_context = pdf_service.get_problem_section(problem_number)
            if not textbook_context:
                print(f"  ⚠️  Problem {problem_number} not found, using full text")
                textbook_context = pdf_service.get_full_text()
        else:
            print("  ⚠️  Problem number not detected, using full text")
            textbook_context = pdf_service.get_full_text()
            problem_number = None
        
        print(f"  ✓ Context size: {len(textbook_context)} characters")
        
        # Step 3: Analyze drawing with Gemini
        print("🤖 Step 3: Analyzing drawing with AI...")
        analysis = gemini_service.analyze_drawing(
            image_bytes,
            textbook_context,
            problem_number
        )
        
        # Add metadata
        analysis['filename'] = file.filename
        analysis['detected_problem'] = problem_number
        analysis['context_used'] = "specific_section" if problem_number else "full_text"
        
        print("✅ Analysis complete!\n")
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
