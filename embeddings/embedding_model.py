# === Imports ===
import chromadb
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
    print("🔵 Inicializando cliente de ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    print("🟢 Cliente de ChromaDB inicializado.")
    
    # Initialize collection
    print("🔵 Creando o cargando colección...")
    collection = client.get_or_create_collection(name="itsmehi_collection")
    print("🟢 Colección cargada o creada.")
    
    # Initialize embedding model
    print("🔵 Cargando modelo de embeddings...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("🟢 Modelo de embeddings cargado.")
    
    # Sample documents (simulate CV + job offer)
    documentos = [
        "Soy analista de datos especializado en procesamiento de lenguaje natural.",
        "Tengo experiencia creando pipelines ETL y dashboards en Power BI.",
        "Buscamos un candidato capaz de analizar feedback textual de clientes.",
        "El rol requiere habilidades en Python, NLP y visualización de datos."
    ]
    
    # Create embeddings
    print("🔵 Generando embeddings de documentos...")
    embeddings = model.encode(documentos).tolist()
    print("🟢 Embeddings generados.")
    
    # Add documents to collection
    print("🔵 Añadiendo documentos a la colección...")
    collection.add(
        documents=documentos,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(documentos))]
    )
    print("🟢 Documentos añadidos a la colección.")

    print("✅ Base de prueba de ChromaDB creada en data/chromadb/")

if __name__ == "__main__":
    crear_chromadb_prueba()
