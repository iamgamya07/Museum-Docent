import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables or .env file.")

# File Paths
INDEX_PATH = "faiss_index"
ARTWORK_DATA_PATH = "data/met_artworks.jsonl"

# Model Names
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama3-8b-8192"