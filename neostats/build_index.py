import os
import sys # Import the sys module
from utils.rag_utils import load_artwork_chunks
from models.embeddings import build_faiss_index

# Define the file paths
JSONL_PATH = os.path.join("data", "met_artworks.jsonl")
INDEX_PATH = "faiss_index"

def main():
    """
    Main function to build and save the FAISS index.
    """
    print("🚀 Starting the indexing process...")

    # 1. Load artwork data from the JSONL file
    print(f"Loading artwork chunks from {JSONL_PATH}...")
    if not os.path.exists(JSONL_PATH):
        print(f"❌ Error: Data file not found at {JSONL_PATH}")
        print("Please run the scraper first by executing: python data/met_scraper.py")
        sys.exit(1) # Exit the script

    chunks = load_artwork_chunks(JSONL_PATH)
    print(f"✅ Successfully loaded {len(chunks)} artwork chunks.")

    # --- THIS IS THE NEW, IMPORTANT PART ---
    # 2. Check if any chunks were loaded before proceeding
    if not chunks:
        print("❌ Error: No artwork data found. The scraper may have failed to collect data.")
        print("Please check the output of 'python data/met_scraper.py' for errors.")
        sys.exit(1) # Exit the script gracefully

    # 3. Build the FAISS index and save it to disk
    print(f"Building FAISS index and saving to '{INDEX_PATH}.index'...")
    build_faiss_index(chunks, index_path=INDEX_PATH)
    print("✅ Indexing complete! Files 'faiss_index.index' and 'faiss_index_chunks.pkl' have been created.")
    print("You can now run the main application.")

if __name__ == "__main__":
    main()