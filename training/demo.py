import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

Gemini_KEY = os.getenv("Gemini_KEY")
genai.configure(api_key=Gemini_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
    