# tests/test_rag_pipeline.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from agent.rag_agent import generar_respuesta

try:
    from langdetect import detect
except ImportError:
    detect = lambda _: "es"

st.title("🔁 RAG Pipeline Test — Simulated Context")

# === Input ===
pregunta = st.text_input("🗣️ Pregunta o instrucción:")

# Only process if there's valid input
if pregunta.strip():
    try:
        idioma_detectado = detect(pregunta)
    except Exception:
        idioma_detectado = "es"

    # Contexto simulado
    contexto_simulado = [
        "La inteligencia artificial es un campo de estudio de la informática centrado en desarrollar sistemas capaces de realizar tareas que normalmente requieren inteligencia humana.",
        "Incluye técnicas como el aprendizaje automático, el procesamiento del lenguaje natural y la visión por computador.",
        "Su objetivo es crear máquinas que puedan razonar, aprender y tomar decisiones."
    ]

    if st.button("Generar respuesta con RAG simulado"):
        with st.spinner("🤖 Pensando..."):
            respuesta = generar_respuesta(contexto_simulado, pregunta.strip(), idioma=idioma_detectado)

        if respuesta:
            st.success("✅ Respuesta generada:")
            st.markdown(respuesta)
        else:
            st.error("❌ No se pudo generar una respuesta.")
else:
    st.info("✍️ Introduce una pregunta para probar el flujo.")
