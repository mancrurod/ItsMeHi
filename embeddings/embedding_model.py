# === Imports ===
from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path

# === Constants ===
CHROMA_DIR = "data/chromadb/"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# === Functions ===

def crear_chromadb_prueba() -> None:
    """Create a simple ChromaDB collection with sample documents."""
    # Ensure directory exists
    print(f"🔵 Intentando crear carpeta en: {CHROMA_DIR}")
    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)
    print("🟢 Carpeta creada o ya existente.")

    # Initialize ChromaDB
    settings = Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=CHROMA_DIR,
        anonymized_telemetry=False
    )
    client = Client(settings)
    
    # Initialize collection
    collection = client.get_or_create_collection(name="itsmehi_collection")
    
    # Initialize embedding model
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Sample documents (simulate CV + job offer)
    documentos = [
        "Soy analista de datos especializado en procesamiento de lenguaje natural.",
        "Tengo experiencia creando pipelines ETL y dashboards en Power BI.",
        "Buscamos un candidato capaz de analizar feedback textual de clientes.",
        "El rol requiere habilidades en Python, NLP y visualización de datos."
    ]
    
    # Create embeddings
    embeddings = model.encode(documentos).tolist()
    
    # Add documents to collection
    collection.add(
        documents=documentos,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(documentos))]
    )
    
    # Save database to disk
    client.persist()

    print("✅ Base de prueba de ChromaDB creada en data/chromadb/")
