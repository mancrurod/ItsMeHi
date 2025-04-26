# vector_db/generate_response_hf.py

import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

# === Connect to Hugging Face Inference API ===
api_token = os.getenv("HF_API_TOKEN")
model_name = os.getenv("HF_GENERATION_MODEL")

client = InferenceClient(token=api_token)

def generar_respuesta_hf(prompt: str) -> str:
    """Generate a response using Hugging Face Inference API."""
    try:
        response = client.text_generation(
            prompt,
            model=model_name,
            max_new_tokens=256,
            temperature=0.7,
            stop_sequences=["###", "</s>"]
        )
        return response.strip()
    except Exception as e:
        print(f"⚡ Error generating response: {e}")
        return "⚡ El modelo no respondió a tiempo. Por favor, inténtalo de nuevo en unos minutos."
