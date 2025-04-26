# === Imports ===
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

# === Constants ===
NOMBRE_COLECCION = "itsmehi_collection"
MODELO_EMBEDDINGS = "sentence-transformers/all-MiniLM-L6-v2"

# === Load environment variables ===
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# === Initialize Qdrant client ===
cliente_qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# === Create or ensure collection ===
if not cliente_qdrant.collection_exists(collection_name=NOMBRE_COLECCION):
    cliente_qdrant.create_collection(
        collection_name=NOMBRE_COLECCION,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )


# === Initialize embedding model ===
modelo_embeddings = SentenceTransformer(MODELO_EMBEDDINGS)

# === Test documents (in Spanish) ===
documentos = [
    "Soy analista de datos especializado en procesamiento de lenguaje natural.",
    "Tengo experiencia creando pipelines ETL y dashboards en Power BI.",
    "Buscamos un candidato capaz de analizar feedback textual de clientes.",
    "El rol requiere habilidades en Python, NLP y visualización de datos."
]

# === Generate embeddings ===
vectores = modelo_embeddings.encode(documentos).tolist()

# === Insert documents into Qdrant ===
cliente_qdrant.upsert(
    collection_name=NOMBRE_COLECCION,
    points=[
        {
            "id": i,
            "vector": vector,
            "payload": {"text": documento}
        }
        for i, (vector, documento) in enumerate(zip(vectores, documentos))
    ]
)

print("✅ Documentos de prueba cargados correctamente en Qdrant Cloud.")
