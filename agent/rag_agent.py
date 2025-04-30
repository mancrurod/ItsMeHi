"""RAG Agent for ItsMeHi App using Qdrant Cloud.

This module handles document retrieval and answer generation
based on recruiter questions.

Functions:
    cargar_qdrant(): Load a Qdrant client from environment variables.
    buscar_contexto_relevante(pregunta, client, k): Retrieve top-k relevant context passages.
    generar_respuesta(contexto, pregunta, idioma): Generate a final answer based on retrieved context and question.
"""

# === Imports ===
import os
from typing import List
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from vector_db.embedding_client import embed_texto
from vector_db.generate_response_hf import generar_respuesta_hf

# Optional: automatic language detection
try:
    from langdetect import detect
except ImportError:
    detect = lambda text: "es"  # fallback to Spanish

# === Load Environment Variables ===
load_dotenv()

# === Constants ===
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
VECTOR_SIZE = 384
COLLECTION_NAME = "itsmehi_collection"
MAX_CONTEXT_LENGTH = 3000  # Limit context length to 3000 characters

# === Qdrant connection ===
def cargar_qdrant() -> QdrantClient:
    """
    Load a Qdrant client connected to Qdrant Cloud.

    Returns:
        QdrantClient: A Qdrant client instance.
    """
    cliente = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    colecciones = cliente.get_collections().collections
    nombres = [col.name for col in colecciones]

    if COLLECTION_NAME not in nombres:
        cliente.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )

    return cliente

# === Context retrieval ===
def buscar_contexto_relevante(pregunta: str, cliente: QdrantClient, k: int = 3) -> List[str]:
    """
    Search Qdrant for the most relevant context fragments given a question.

    Args:
        pregunta (str): The user's question.
        cliente (QdrantClient): Connected Qdrant client.
        k (int): Number of top documents to retrieve.

    Returns:
        List[str]: List of relevant text fragments.
    """
    vector_consulta = embed_texto(pregunta)

    if not vector_consulta:
        print("⚡ Failed to generate embedding.")
        return []

    resultados = cliente.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector_consulta,
        limit=k,
    )

    return [hit.payload["text"] for hit in resultados]

# === Answer generation ===
def generar_respuesta(contexto: List[str], pregunta: str, idioma: str = "") -> str:
    """
    Generate a natural-language answer using retrieved context and the user's question.

    Args:
        contexto (List[str]): Retrieved context fragments.
        pregunta (str): The user's question.
        idioma (str, optional): Language code ("es", "en"). If empty, auto-detected.

    Returns:
        str: The generated answer.
    """
    contexto_unido = "\n".join(contexto)

    if len(contexto_unido) > MAX_CONTEXT_LENGTH:
        contexto_unido = contexto_unido[:MAX_CONTEXT_LENGTH]

    if not idioma:
        try:
            idioma = detect(pregunta)
        except Exception:
            idioma = "es"

    if idioma == "en":
        prompt = (
            f"Use the following context to answer clearly and helpfully.\n\n"
            f"Context:\n{contexto_unido}\n\n"
            f"Question: {pregunta}\n"
            f"Answer:"
        )
    else:
        prompt = (
            f"Usa el siguiente contexto para responder con claridad y precisión.\n\n"
            f"Contexto:\n{contexto_unido}\n\n"
            f"Pregunta: {pregunta}\n"
            f"Respuesta:"
        )

    try:
        respuesta = generar_respuesta_hf(prompt)
        return respuesta or "⚠️ No se pudo generar una respuesta útil."
    except Exception:
        return "⚡ El modelo no respondió a tiempo. Intenta nuevamente."
