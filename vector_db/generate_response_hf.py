# vector_db/generate_response_hf.py

import os
import logging
import sys
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import streamlit as st
import traceback

# === Load environment variables ===
load_dotenv()

# === Setup logger ===
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# === Connect to Hugging Face Inference API ===
api_token = os.getenv("HF_API_TOKEN")
model_name = os.getenv("HF_GENERATION_MODEL")

client = InferenceClient(token=api_token)

def generar_respuesta_hf(prompt: str) -> str:
    """Generate a response using Hugging Face Inference API with forced error visibility."""
    try:
        logger.debug(f"🚀 Enviando prompt a HuggingFace (primeros 100 chars): {prompt[:100]}...")
        response = client.text_generation(
            prompt,
            model=model_name,
            max_new_tokens=256,
            temperature=0.7,
            stop_sequences=["###", "</s>"],
            timeout=30,
        )
        logger.debug("✅ Respuesta recibida de HuggingFace.")
        return response.strip()
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error(f"⚡ Error real capturado:\n{error_trace}")
        st.error(f"⚡ Error interno de generación: {str(e)}")
        raise e  # 👈 Forzar re-lanzar la excepción para que Streamlit lo capture sí o sí
