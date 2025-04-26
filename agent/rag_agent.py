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
from sentence_transformers import SentenceTransformer
# Load model forcing CPU
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from google.generativeai import GenerativeModel
from google.api_core.exceptions import ResourceExhausted
import google.generativeai as genai

# === Load Environment Variables ===
load_dotenv()

# === Configure Gemini ===
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# === Constants ===
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
VECTOR_SIZE = 384  # Assuming you use 'all-MiniLM-L6-v2' model
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

def buscar_contexto_relevante(pregunta: str, client: QdrantClient, model: SentenceTransformer, k: int = 3) -> List[str]:
    """Retrieve the most relevant context passages given a question.

    Args:
        pregunta (str): Recruiter's question.
        client (QdrantClient): Connected Qdrant client.
        model (SentenceTransformer): Model to embed the question.
        k (int): Number of context chunks to retrieve.

    Returns:
        List[str]: List of retrieved context passages.
    """
    query_vector = model.encode(pregunta).tolist()

    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=k,
    )

    documentos = [hit.payload["text"] for hit in search_result]
    return documentos


def generar_respuesta(contexto: List[str], pregunta: str) -> str:
    """Generate a response using Gemini based on the retrieved context and the question.

    Args:
        contexto (List[str]): Retrieved context documents.
        pregunta (str): Original question.

    Returns:
        str: Generated response.
    """
    contexto_unido = "\n".join(contexto)

    modelo = GenerativeModel(model_name="gemini-1.5-flash-latest")

    prompt = (
        f"Usando \u00fanicamente la siguiente informaci\u00f3n de contexto:\n\n"
        f"{contexto_unido}\n\n"
        f"Responde de forma clara y profesional a esta pregunta:\n"
        f"{pregunta}"
    )

    try:
        respuesta = modelo.generate_content(prompt)
        return respuesta.text.strip()
    except ResourceExhausted:
        return "🚦 Hemos alcanzado el l\u00edmite de generaci\u00f3n de respuestas por minuto. Por favor, espere unos segundos y vuelva a intentarlo."
