from typing import List
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

# Load embedding model once
tokenizer_model = "all-MiniLM-L6-v2"
model = SentenceTransformer(tokenizer_model)

def build_faiss_index(text_chunks: List[str], index_path: str = None):
    """
    Generate embeddings and store them in a FAISS index.
    Optionally save index and mapping.
    """
    embeddings = model.encode(text_chunks, show_progress_bar=True)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    if index_path:
        faiss.write_index(index, f"{index_path}.index")
        with open(f"{index_path}_chunks.pkl", "wb") as f:
            pickle.dump(text_chunks, f)

    return index, text_chunks

def load_faiss_index(index_path: str):
    """
    Load FAISS index and corresponding text chunks.
    """
    index = faiss.read_index(f"{index_path}.index")
    with open(f"{index_path}_chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def embed_query(query: str):
    """
    Embed a query string for retrieval.
    """
    return model.encode([query])[0]
