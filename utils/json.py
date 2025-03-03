import json
import re

def extract_json_from_response(response_text):
    """
    Extract JSON from the model response, handling possible code blocks.
    
    Args:
        response_text: Raw text response from the model
        
    Returns:
        dict: Parsed JSON object or None if parsing fails
    """
    # Try to parse as is first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from code blocks
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find anything that looks like JSON
    json_match = re.search(r'({[\s\S]*})', response_text)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    return None
