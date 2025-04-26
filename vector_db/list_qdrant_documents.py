# === Imports ===
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

# === Constants ===
NOMBRE_COLECCION = "itsmehi_collection"

# === Load environment variables ===
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# === Initialize Qdrant client ===
cliente_qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# === List documents in collection ===
resultados, _ = cliente_qdrant.scroll(
    collection_name=NOMBRE_COLECCION,
    limit=100  # You can increase if needed
)

print(f"✅ Documentos encontrados en '{NOMBRE_COLECCION}':\n")

for punto in resultados:
    print(f"ID: {punto.id} | Texto: {punto.payload['text']}")
