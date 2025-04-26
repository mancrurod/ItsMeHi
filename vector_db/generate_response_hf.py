# vector_db/generate_response_hf.py

import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import streamlit as st
import traceback

# === Load environment variables ===
load_dotenv()

# === Connect to Hugging Face Inference API ===
api_token = os.getenv("HF_API_TOKEN")
model_name = os.getenv("HF_GENERATION_MODEL")

client = InferenceClient(token=api_token)

def generar_respuesta_hf(prompt: str) -> str:
    """Generate a response using Hugging Face Inference API with timeout control."""
    try:
        print(f"🚀 Enviando prompt a HuggingFace...")
        # Hacemos llamada limitada a máximo 30 segundos
        response = client.text_generation(
            prompt,
            model=model_name,
            max_new_tokens=256,
            temperature=0.7,
            stop_sequences=["###", "</s>"],
            timeout=30,  # ⏱️ Forzar timeout de cliente
        )
        print(f"✅ Respuesta recibida de HuggingFace.")
        return response.strip()
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"⚡ Error real capturado:\n{error_trace}")
        st.error(f"⚡ Error interno de generación: {str(e)}")
        return "⚡ El modelo no respondió o tardó demasiado. Por favor, intenta de nuevo más tarde."
