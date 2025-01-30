import os
import google.generativeai as genai

# Load API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key not found! Make sure GEMINI_API_KEY is set.")

genai.configure(api_key=api_key)

# Use the correct model for image processing
model = genai.GenerativeModel("gemini-1.5-pro-vision")

def analyze_image(image_path):
    # Open the image file
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()

    # Send the image data to Gemini API
    response = model.generate_content([image_data])

    return response.text if response.text else "No response from Gemini"
