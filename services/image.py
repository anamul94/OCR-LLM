from fastapi import UploadFile, HTTPException

async def validate_and_process_image(file: UploadFile):
    """
    Validate image file and prepare it for Gemini processing.
    
    Args:
        file: Uploaded image file
        
    Returns:
        dict: Processed image data ready for Gemini
        
    Raises:
        HTTPException: If file type is invalid
    """
    # Read file content
    contents = await file.read()
    
    # Check file type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=400, 
            detail="Only JPEG and PNG images are supported"
        )
    
    # Prepare image for processing
    image_parts = input_image_setup(contents, file.content_type)
    return image_parts

def input_image_setup(file_content, content_type):
    """
    Prepare image for Gemini API.
    
    Args:
        file_content: Binary content of the file
        content_type: MIME type of the file
        
    Returns:
        list: Formatted image data for Gemini
    """
    image_parts = [
        {
            "mime_type": content_type,
            "data": file_content
        }
    ]
    return image_parts
