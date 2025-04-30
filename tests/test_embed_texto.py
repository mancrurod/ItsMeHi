# test_embed_texto.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from vector_db.embedding_client import embed_texto

st.title("🧪 Embedding Test — Hugging Face")

texto_entrada = st.text_area("✏️ Introduce un texto para generar su embedding:")

if st.button("Generar embedding"):
    if texto_entrada.strip():
        with st.spinner("🔄 Generando embedding..."):
            vector = embed_texto(texto_entrada.strip())

        if vector:
            st.success(f"✅ Embedding generado con {len(vector)} dimensiones.")
            st.code(vector[:10], language="python")  # Mostrar solo primeros 10 valores
        else:
            st.error("❌ No se pudo generar el embedding. Revisa el modelo o el token.")
    else:
        st.warning("⚠️ Introduce algún texto antes de continuar.")
