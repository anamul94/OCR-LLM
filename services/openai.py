import os
import openai
from api.models import Category, ErrorResponse
from utils.json import extract_json_from_response
from utils.constants import FOOD_PROMPT, MEDICAL_PROMPT

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_with_openai(image_parts, category: Category) -> dict:
    """
    Analyze an image using OpenAI's GPT model.
    
    Args:
        image_parts: Processed image data for OpenAI
        category: Type of analysis to perform (food or medical)
        
    Returns:
        dict: Structured analysis results
    """
    # Select prompt based on category
    prompt = FOOD_PROMPT if category == Category.FOOD else MEDICAL_PROMPT
    
    # Get response from model
    response_text = get_openai_response(prompt, image_parts)
    
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

def get_openai_response(prompt, image_parts):
    """
    Get response from OpenAI's GPT model.
    
    Args:
        prompt: Text prompt for the model
        image_parts: Image data for the model
        
    Returns:
        str: Text response from the model
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are an AI assistant that provides structured JSON responses."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": image_parts[0]}  # Assuming the first image part contains the URL
            ]}
        ],
        max_tokens=1000
    )
    
    return response["choices"][0]["message"]["content"]
