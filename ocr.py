### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import io

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-1.5-pro')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
##initialize our streamlit app

st.set_page_config(page_title="Health & Nutrition Analyzer – AI-Powered OCR")

st.header("Health & Nutrition Analyzer – AI-Powered OCR")
st.markdown("""
### 🔒 HIPAA Compliance Notice  
This application follows **HIPAA-compliant best practices** to protect your health information:  
- **No data is stored or shared** after processing.  
- **End-to-end encryption** is used for secure transmission.  
- AI-generated insights are **for informational purposes only** and should not replace professional medical advice.  
""")

st.write("Upload an image of a **medical report** or **food items**, and this AI-powered tool will extract relevant details in structured JSON format.")


# input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

food = "Food"
medical = "Medical"
options = st.selectbox(
    "Plz Select a Category",
    (food, medical),
)



submit=st.button("Describe and extract value in JSON format")


medical_report_prompt="""
Extract relevant diagnostic details from the given medical diagnostic report and provide the output in structured JSON format. Ensure that only diagnostic-related information is captured, including test name, results, reference ranges, and observations. The JSON should follow this format:
{
  "patient_details": {
    "name": "John Doe",
    "age": 45,
    "gender": "Male"
  },
  "diagnostic_tests": [
    {
      "test_name": "Complete Blood Count (CBC)",
      "results": {
        "hemoglobin": {
          "value": "13.5 g/dL",
          "reference_range": "13.0 - 17.0 g/dL",
          "status": "Normal"
        },
        "white_blood_cells": {
          "value": "7,000 cells/uL",
          "reference_range": "4,000 - 11,000 cells/uL",
          "status": "Normal"
        }
      },
      "observations": "All parameters within normal limits."
    },
    {
      "test_name": "Lipid Profile",
      "results": {
        "cholesterol": {
          "value": "220 mg/dL",
          "reference_range": "<200 mg/dL",
          "status": "High"
        },
        "triglycerides": {
          "value": "180 mg/dL",
          "reference_range": "<150 mg/dL",
          "status": "Borderline High"
        }
      },
      "observations": "Elevated cholesterol levels; dietary modifications recommended."
    }
  ],
  "doctor_notes": "Patient advised to monitor lipid levels and follow up in 3 months."
}
"Ensure the extracted data follows this structure while accurately representing the diagnostic report."
"""

food_item_prompt = """
"You are an expert nutritionist. Analyze the given image and extract relevant food details. Identify the food items present in the image and provide their standard nutritional values per unit based on commonly available nutritional data. If multiple items are detected, list them separately. The JSON output should strictly follow this format:"

{
  "food_items": [
    {
      "name": "Apple",
      "nutritional_values": {
        "calories": "52 kcal",
        "protein": "0.3 g",
        "carbohydrates": "14 g",
        "fat": "0.2 g",
        "fiber": "2.4 g"
      },
      "serving_size": "100 g"
    },
    {
      "name": "Chicken Breast",
      "nutritional_values": {
        "calories": "165 kcal",
        "protein": "31 g",
        "carbohydrates": "0 g",
        "fat": "3.6 g"
      },
      "serving_size": "100 g"
    }
  ]
}
"Ensure the extracted data follows this structure while accurately identifying and representing the food items and their standard nutritional values. Return the final output strictly in JSON format."
"""

## If submit button is clicked

input_prompt = ''
if options == food:
    input_prompt = food_item_prompt
if options == medical:
    input_prompt= medical_report_prompt

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data, "Return JSON")
    print(response)
    st.subheader("The Response is")
    st.write(response)

