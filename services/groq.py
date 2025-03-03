import os
from groq import Groq
from api.models import Category, ErrorResponse
from utils.json import extract_json_from_response
from utils.constants import FOOD_PROMPT, MEDICAL_PROMPT

# Configure Groq API
# groq.api_key = os.getenv("GROQ_API_KEY")

def analyze_with_groq(image_parts, category: Category) -> dict:
    """
    Analyze an image using Groq's AI model.
    
    Args:
        image_parts: Processed image data for Groq
        category: Type of analysis to perform (food or medical)
        
    Returns:
        dict: Structured analysis results
    """
    # Select prompt based on category
    prompt = FOOD_PROMPT if category == Category.FOOD else MEDICAL_PROMPT
    
    # Get response from model
    response_text = get_groq_response(prompt, image_parts)
    
    # Try to extract and parse JSON from the response
    parsed_json = extract_json_from_response(response_text)
    
    if parsed_json:
        return parsed_json
    else:
        # Log the raw response for debugging
        print("Failed to parse JSON. Raw response:", response_text)
        
        # Return error response
        error_response = ErrorResponse(
            status=False,
            message="Error parsing AI response"
        )
        
        # Add debug info if in debug mode
        if os.getenv("DEBUG_MODE") == "true":
            error_response.debug_info = {
                "response_preview": response_text[:200] + "..." if len(response_text) > 200 else response_text
            }
            
        return error_response.dict(exclude_none=True)

def get_groq_response(prompt, image_parts):
    """
    Get response from Groq's AI model.
    
    Args:
        prompt: Text prompt for the model
        image_parts: Image data for the model
        
    Returns:
        str: Text response from the model
    """
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an AI assistant that provides structured JSON responses."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": image_parts[0]}
                # Assuming the first image part contains the URL
            ]}
        ],
        max_tokens=1000
    )
    print("*************GROQ RESPONSE*************")
    print(response)
    return response["choices"][0]["message"]["content"]