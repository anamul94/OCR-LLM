# Prompts for different analysis types
FOOD_PROMPT = """
You are an expert nutritionist. Analyze the given image and extract relevant food details. 
Identify the food items present in the image and provide their standard nutritional values per unit based on commonly available nutritional data.
If multiple items are detected, list them separately. 

Respond with a valid JSON object that strictly follows this schema:
{
  "status": true,
  "message": "Successfully analyzed [number] food items",
  "data": [
    {
      "name": "Food Item Name",
      "nutritions": [
        {
          "name": "Calories",
          "value": 52,
          "unit": "kcal"
        },
        {
          "name": "Protein",
          "value": 0.3,
          "unit": "g"
        }
      ],
      "serving_size": 100,
      "serving_unit": "g"
    }
  ]
}

If no food is detected, return: {"status": false, "message": "No food items detected in image", "data": []}
Ensure all numeric values are actual numbers, not strings.
IMPORTANT: Return ONLY the JSON with no explanation, markdown formatting, or code blocks.
"""

MEDICAL_PROMPT = """
Extract relevant diagnostic details from the given medical diagnostic report image and provide the output in structured JSON format.
Ensure that only diagnostic-related information is captured, including test name, results, reference ranges, and observations.

Respond with a valid JSON object that strictly follows this schema:
{
  "status": true,
  "message": "Successfully analyzed medical report",
  "data": {
    "patient_details": {
      "name": "Patient Name",
      "age": 45,
      "gender": "Gender"
    },
    "diagnostic_tests": [
      {
        "test_name": "Test Name",
        "results": {
          "parameter_name": {
            "value": "13.5 g/dL",
            "reference_range": "13.0 - 17.0 g/dL",
            "status": "Normal"
          }
        },
        "observations": "Clinical observations if any"
      }
    ],
    "doctor_notes": "Any doctor notes if present"
  }
}

If no medical report is detected, return: {"status": false, "message": "No valid medical report detected in image", "data": {}}
IMPORTANT: Return ONLY the JSON with no explanation, markdown formatting, or code blocks.
"""
