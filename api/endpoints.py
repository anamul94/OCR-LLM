import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from api.models import Category, BaseResponse
from services.gemini import analyze_with_gemini
from services.groq import analyze_with_groq
from services.image import validate_and_process_image

router = APIRouter(
    prefix="/api/v1",
    tags=["analyze"]
)

@router.get("/", response_model=dict)
async def root():
    """API root endpoint with basic information."""
    return {
        "name": "Health & Nutrition Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "/api/analyze": "POST - Analyze food or medical images"
        }
    }

@router.post("/analyze", response_model=dict)
async def analyze_image(
    file: UploadFile = File(...),
    category: Category = Form(...)
):
    """
    Analyze an image for food nutritional information or medical report data.
    
    - **file**: The image file to analyze
    - **category**: Type of analysis to perform (food or medical)
    
    Returns a structured JSON response with the analysis results.
    """
    try:
        # Validate and process the uploaded image
        image_parts = await validate_and_process_image(file)
        
        # Analyze the image using Gemini
        # result = analyze_with_gemini(image_parts, category)
        result = analyze_with_gemini(image_parts, category)
        
        return result
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
