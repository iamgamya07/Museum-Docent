import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables or .env file.")
