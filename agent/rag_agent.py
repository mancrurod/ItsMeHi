"""RAG Agent for ItsMeHi App.

This module handles document retrieval and answer generation
based on recruiter questions.

Functions:
    cargar_chromadb(path_db): Load and return a ChromaDB collection from disk.
    buscar_contexto_relevante(pregunta, collection, k): Retrieve top-k relevant context passages.
    generar_respuesta(contexto, pregunta): Generate a final answer based on retrieved context and question.
"""

# === Imports ===
from chromadb import Client
from chromadb.config import Settings
from google.generativeai import GenerativeModel
from typing import List

# === Functions ===

def cargar_chromadb(path_db: str) -> Client:
    """Load a ChromaDB collection from the specified path.

    Args:
        path_db (str): Path to the ChromaDB persistent folder.

    Returns:
        Client: A ChromaDB client instance ready for querying.
    """
    settings = Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=path_db,
        anonymized_telemetry=False
    )
    client = Client(settings)
    return client


def buscar_contexto_relevante(pregunta: str, collection: Client, k: int = 3) -> List[str]:
    """Retrieve the most relevant context passages given a question.

    Args:
        pregunta (str): Recruiter's question.
        collection (Client): Loaded ChromaDB collection.
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
    """Generate a response using Gemini based on the retrieved context and the question.

    Args:
        contexto (List[str]): Retrieved context passages.
        pregunta (str): Recruiter's question.

    Returns:
        str: Final generated answer.
    """
    # Join context passages into a single string
    contexto_unido = "\n".join(contexto)
    
    # Initialize Gemini model
    modelo = GenerativeModel(model_name="gemini-1.5-flash-latest")
    
    # Prompt engineering
    prompt = (
        f"Usando únicamente la siguiente información de contexto:\n\n"
        f"{contexto_unido}\n\n"
        f"Responde de forma clara y profesional a esta pregunta:\n"
        f"{pregunta}"
    )
    
    # Generate response
    respuesta = modelo.generate_content(prompt)
    return respuesta.text.strip()
