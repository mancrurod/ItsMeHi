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

# === Delete collection ===
cliente_qdrant.delete_collection(collection_name=NOMBRE_COLECCION)

print(f"🧹 Colección '{NOMBRE_COLECCION}' eliminada correctamente de Qdrant Cloud.")
