# vector_db/embedding_client.py

import os
from typing import List
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import streamlit as st

# === Load environment variables ===
load_dotenv()

# === Constants ===
token_api = os.getenv("HF_API_TOKEN")
modelo_embeddings = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# === Cached Hugging Face client ===
@st.cache_resource(show_spinner="🔗 Connecting to Hugging Face embedding model...")
def get_cliente_inferencia() -> InferenceClient:
    return InferenceClient(token=token_api)

# === Embedding function ===
def embed_texto(texto: str) -> List[float]:
    """
    Generate an embedding vector for a given input text using Hugging Face Inference API.

    Args:
        texto (str): The text to embed.

    Returns:
        List[float]: The embedding vector as a list of floats, or an empty list on failure.
    """
    if not texto:
        return []

    cliente = get_cliente_inferencia()

    try:
        embedding = cliente.feature_extraction(text=texto, model=modelo_embeddings)

        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()

        if not embedding or not isinstance(embedding, list):
            raise ValueError("⚠️ Invalid or empty embedding.")

        return embedding

    except Exception as error:
        print(f"⚡ Error generating embedding: {error}")
        return None
