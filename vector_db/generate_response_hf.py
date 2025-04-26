# vector_db/generate_response_hf.py

import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import streamlit as st

# === Load environment variables ===
load_dotenv()

# === Connect to Hugging Face Inference API ===
api_token = os.getenv("HF_API_TOKEN")
model_name = os.getenv("HF_GENERATION_MODEL")

client = InferenceClient(token=api_token)

def generar_respuesta_hf(prompt: str) -> str:
    """Generate a response using Hugging Face Inference API with detailed debugging."""
    try:
        print(f"🚀 Enviando prompt a HuggingFace: {prompt[:100]}...")  # Solo mostramos los primeros 100 caracteres
        response = client.text_generation(
            prompt,
            model=model_name,
            max_new_tokens=256,
            temperature=0.7,
            stop_sequences=["###", "</s>"]
        )
        print(f"✅ Respuesta recibida de HuggingFace.")
        return response.strip()
    except Exception as e:
        error_message = f"⚡ Error real generado: {str(e)}"
        print(error_message)
        st.error(error_message)  # Mostrarlo en Streamlit también
        return "⚡ El modelo no respondió a tiempo. Por favor, inténtalo de nuevo en unos minutos."
