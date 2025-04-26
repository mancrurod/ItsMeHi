import os
import logging
import httpx
from typing import List
from huggingface_hub import InferenceClient

# === Create a reusable client with timeout and retries ===
client = httpx.Client(
    timeout=httpx.Timeout(20.0, connect=10.0),  # 20s total timeout, 10s to connect
    limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
    transport=httpx.HTTPTransport(retries=3),   # 3 automatic retries
)

# === Configure Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Load Environment Variables ===
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_GENERATION_MODEL = os.getenv("HF_GENERATION_MODEL")

# === Initialize Hugging Face Client ===
client = InferenceClient(token=HF_API_TOKEN)

# === Constants ===
MAX_OUTPUT_TOKENS = 100

def generar_respuesta_hf(contexto: str, pregunta: str) -> str:
    payload = {
        "inputs": f"Context: {contexto}\n\nQuestion: {pregunta}",
        "parameters": {"max_new_tokens": 200},
    }
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = client.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data[0]["generated_text"] if data else "⚠️ No response generated."
    except Exception as e:
        logger.error(f"❌ HuggingFace request failed: {e}")
        return "⚠️ Unable to generate a response at the moment."