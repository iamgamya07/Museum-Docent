import json
import os
from typing import List
from models.embeddings import embed_query, load_faiss_index
import numpy as np

def load_artwork_chunks(jsonl_path: str) -> List[str]:
    """
    Loads artwork metadata from a JSONL file and converts each entry into a text chunk.
    """
    chunks = []

    if not os.path.exists(jsonl_path):
        raise FileNotFoundError(f"File not found: {jsonl_path}")

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)

                title = data.get("title", "Unknown Title")
                artist = data.get("artist", "Unknown Artist")
                date = data.get("date", "Unknown Date")
                medium = data.get("medium", "Unknown Medium")
                dimensions = data.get("dimensions", "")
                description = data.get("description", "")
                url = data.get("url", "")

                text_chunk = f"""
                Title: {title}
                Artist: {artist}
                Date: {date}
                Medium: {medium}
                Dimensions: {dimensions}
                Description: {description}
                Source: {url}
                """
                chunks.append(text_chunk.strip())

            except json.JSONDecodeError:
                continue  # Skip malformed lines

    return chunks


def retrieve_similar_artworks(query: str, index_path: str, top_k: int = 3) -> List[str]:
    """
    Retrieve top-k most similar artwork chunks based on the query.
    """
    index, chunks = load_faiss_index(index_path)
    query_vec = embed_query(query).reshape(1, -1)
    distances, indices = index.search(query_vec, top_k)

    return [chunks[i] for i in indices[0] if i < len(chunks)]
