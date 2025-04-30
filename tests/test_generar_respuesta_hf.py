# test_generar_respuesta_hf.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from vector_db.generate_response_hf import generar_respuesta_hf

st.title("🤖 Hugging Face Text Generation Test")

prompt = st.text_area("✍️ Write a prompt for the generation model:")

max_tokens = st.slider("🔢 Max tokens to generate:", min_value=16, max_value=512, value=128, step=16)

if st.button("Generate response"):
    if prompt.strip():
        with st.spinner("🧠 Thinking..."):
            respuesta = generar_respuesta_hf(prompt.strip(), max_tokens=max_tokens)

        if respuesta:
            st.success("✅ Response generated successfully!")
            st.markdown(f"**Output:**\n\n{respuesta}")
        else:
            st.error("❌ No response generated. Check model name or token.")
    else:
        st.warning("⚠️ Please enter a prompt first.")
