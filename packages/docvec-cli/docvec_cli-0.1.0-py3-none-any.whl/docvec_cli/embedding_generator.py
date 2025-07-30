from sentence_transformers import SentenceTransformer
import numpy as np
import os

DEFAULT_EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

def load_embedding_model(model_name: str = DEFAULT_EMBEDDING_MODEL) -> SentenceTransformer:

    print(f"Loading embedding model: {model_name}...")
    try:
        model = SentenceTransformer(model_name)
        print(f"Model '{model_name}' loaded successfully.")
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load embedding model '{model_name}': {e}")

def generate_embeddings(texts: list[str], model: SentenceTransformer) -> np.ndarray:
    """
    Generates embeddings for a list of text chunks using the provided model.

    Args:
        texts (list[str]): A list of text chunks.
        model (SentenceTransformer): The loaded SentenceTransformer model.

    Returns:
        np.ndarray: A NumPy array containing the embeddings, where each row
                    corresponds to an embedding for a text chunk.
    """
    if not texts:
        return np.array([])

    print(f"Generating embeddings for {len(texts)} text chunks...")
    try:
        embeddings = model.encode(texts, show_progress_bar=True)
        print("Embeddings generated successfully.")
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Failed to generate embeddings: {e}")