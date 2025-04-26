# vector_db/embedding_client.py

import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from typing import List

# === Load environment variables ===
load_dotenv()

# === Connect to Hugging Face Inference API ===
api_token = os.getenv("HF_API_TOKEN")
model_name = os.getenv("HF_EMBEDDING_MODEL")

client = InferenceClient(token=api_token)

def embed_text(text: str) -> List[float]:
    """Generate embeddings using Hugging Face Inference API."""
    if not text:
        return []
    try:
        embedding = client.feature_extraction(text=text, model=model_name)
        
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()

        if not embedding or not isinstance(embedding, list):
            raise ValueError("Embedding failed or empty.")

        return embedding
    except Exception as e:
        logger.error(f"⚡ Error generating embedding: {e}")
        return None

