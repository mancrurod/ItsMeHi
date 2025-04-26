"""RAG Agent for ItsMeHi App using Qdrant Cloud.

This module handles document retrieval and answer generation
based on recruiter questions.

Functions:
    cargar_qdrant(): Load a Qdrant client from environment variables.
    buscar_contexto_relevante(pregunta, collection_name, model, k): Retrieve top-k relevant context passages.
    generar_respuesta(contexto, pregunta): Generate a final answer based on retrieved context and question.
"""

# === Imports ===
import os
from typing import List

from dotenv import load_dotenv
from vector_db.embedding_client import embed_text

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from vector_db.generate_response_hf import generar_respuesta_hf


# === Load Environment Variables ===
load_dotenv()

# === Constants ===
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
VECTOR_SIZE = 384
COLLECTION_NAME = "itsmehi_collection"

# === Functions ===

from qdrant_client.models import Distance, VectorParams

def cargar_qdrant() -> QdrantClient:
    """Load a Qdrant client connected to Qdrant Cloud.

    Returns:
        QdrantClient: A Qdrant client instance.
    """
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

    # Check if the collection already exists
    colecciones = client.get_collections().collections
    nombres_colecciones = [col.name for col in colecciones]

    if "itsmehi_collection" not in nombres_colecciones:
        client.create_collection(
            collection_name="itsmehi_collection",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    return client

def buscar_contexto_relevante(pregunta: str, client: QdrantClient, k: int = 3) -> List[str]:
    query_vector = embed_text(pregunta)

    if not query_vector:
        print("⚡ No se pudo generar el embedding. Reintentar más tarde.")
        return []

    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=k,
    )

    documentos = [hit.payload["text"] for hit in search_result]
    return documentos

MAX_CONTEXT_LENGTH = 3000  # Limitar a 3000 caracteres

def generar_respuesta(contexto: List[str], pregunta: str) -> str:
    """Generate a response using Hugging Face Inference API based on retrieved context and the question."""
    contexto_unido = "\n".join(contexto)

    # Cut context if it's too large
    if len(contexto_unido) > MAX_CONTEXT_LENGTH:
        contexto_unido = contexto_unido[:MAX_CONTEXT_LENGTH]

    prompt = (
        f"Usa la siguiente información de contexto para responder de forma clara y profesional.\n\n"
        f"Contexto:\n{contexto_unido}\n\n"
        f"Pregunta: {pregunta}\n"
        f"Respuesta:"
    )

    try:
        respuesta = generar_respuesta_hf(prompt)
        return respuesta
    except Exception:
        return "⚡ El modelo no respondió a tiempo. Por favor, inténtalo de nuevo en unos minutos."