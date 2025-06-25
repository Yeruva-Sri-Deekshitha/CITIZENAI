import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils.text_cleaning import clean_text

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API token not found in environment variables.")

# Configure the API key
genai.configure(api_key=api_key)

# Initialize the model (use "gemini-1.5-pro" or "gemini-pro" based on availability)
model = genai.GenerativeModel("gemini-2.5-flash")

# Create a chat session
chat = model.start_chat(history=[])

def generate_response(user_input):
    try:
        cleaned_input = clean_text(user_input)
        response = chat.send_message(cleaned_input)
        return response.text
    except Exception as e:
        print("[ERROR in generate_response]:", e)
        return "Sorry, I couldn't process your request right now."
