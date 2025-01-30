import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# AI Response Function
def get_gemini_response(prompt, img=None):
    model = genai.GenerativeModel("gemini-1.5-flash")

    if img:
        response = model.generate_content([prompt, img])
    else:
        response = model.generate_content(prompt)

    return response.text if response else "Sorry, I couldn't understand."
