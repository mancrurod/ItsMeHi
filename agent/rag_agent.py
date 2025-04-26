"""RAG Agent for ItsMeHi App.

This module handles document retrieval and answer generation
based on recruiter questions.

Functions:
    cargar_chromadb(path_db): Load a ChromaDB persistent client from the specified path.
    buscar_contexto_relevante(pregunta, collection, k): Retrieve top-k relevant context passages.
    generar_respuesta(contexto, pregunta): Generate a final answer based on retrieved context and question.
"""

# === Imports ===
import os
import chromadb
from chromadb.api.models import Collection
from sentence_transformers import SentenceTransformer
from typing import List
from google.generativeai import GenerativeModel
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

# === Load API Key ===

load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# === Functions ===

def cargar_chromadb(path_db: str) -> chromadb.PersistentClient:
    """Load a ChromaDB persistent client from the specified path.

    Args:
        path_db (str): Path to the ChromaDB persistent folder.

    Returns:
        chromadb.PersistentClient: A ChromaDB persistent client instance.
    """
    client = chromadb.PersistentClient(path=path_db)
    return client


def buscar_contexto_relevante(pregunta: str, collection: Collection, k: int = 3) -> List[str]:
    """Retrieve the most relevant context passages given a question.

    Args:
        pregunta (str): Recruiter's question.
        collection (Collection): Loaded ChromaDB collection.
        k (int): Number of context chunks to retrieve.

    Returns:
        List[str]: List of retrieved context passages.
    """
    resultados = collection.query(
        query_texts=[pregunta],
        n_results=k
    )
    documentos = resultados["documents"][0]
    return documentos


def generar_respuesta(contexto: List[str], pregunta: str) -> str:
    """Generate a response using Gemini based on the retrieved context and the question."""
    contexto_unido = "\n".join(contexto)
    
    modelo = GenerativeModel(model_name="gemini-1.5-flash-latest")
    
    prompt = (
        f"Usando únicamente la siguiente información de contexto:\n\n"
        f"{contexto_unido}\n\n"
        f"Responde de forma clara y profesional a esta pregunta:\n"
        f"{pregunta}"
    )

    try:
        respuesta = modelo.generate_content(prompt)
        return respuesta.text.strip()
    except ResourceExhausted:
        return "🚦 Hemos alcanzado el límite de generación de respuestas por minuto. Por favor, espere unos segundos y vuelva a intentarlo."
