import os
from utils.rag_utils import load_artwork_chunks
from models.embeddings import build_faiss_index
from config.config import ARTWORK_DATA_PATH, INDEX_PATH

def main():
    """
    Main function to load data, build, and save the FAISS index.
    """
    if not os.path.exists(ARTWORK_DATA_PATH):
        print(f"Artwork data file not found at: {ARTWORK_DATA_PATH}")
        print("Please run 'python met_scraper.py' first to generate it.")
        return

    print("Loading artwork data...")
    chunks = load_artwork_chunks(ARTWORK_DATA_PATH)

    if not chunks:
        print("No chunks were loaded. Please check the content of your .jsonl file.")
        return

    print(f"Building FAISS index from {len(chunks)} chunks...")
    build_faiss_index(chunks, index_path=INDEX_PATH)

    print(f"FAISS index and chunks saved to '{INDEX_PATH}.index' and '{INDEX_PATH}_chunks.pkl'")

if __name__ == "__main__":
    main()