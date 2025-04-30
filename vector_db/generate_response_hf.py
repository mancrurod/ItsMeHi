"""
generate_response_hf.py (versión local)

Loads a local Hugging Face model and generates responses to user prompts.
"""

# === Imports ===
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# === Model loader with cache ===
@st.cache_resource(show_spinner="🔄 Loading local model (flan-t5-base)...")
def cargar_modelo():
    ruta = "models/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(ruta)
    modelo = AutoModelForSeq2SeqLM.from_pretrained(ruta)
    return pipeline("text2text-generation", model=modelo, tokenizer=tokenizer)

# === Generation function ===
def generar_respuesta_hf(prompt: str, max_tokens: int = 256) -> str:
    """
    Generate a response from a local text generation model.

    Args:
        prompt (str): Input prompt or question.
        max_tokens (int): Maximum tokens to generate.

    Returns:
        str: Generated text response.
    """
    generador = cargar_modelo()
    resultado = generador(prompt, max_new_tokens=max_tokens, do_sample=False)[0]["generated_text"]
    return resultado
