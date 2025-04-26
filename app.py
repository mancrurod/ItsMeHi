"""Main application for ItsMeHi.

This module runs the Streamlit web application, coordinating
the user interface, retrieval system, and logging functionalities.

Functions:
    main(): Entry point for running the Streamlit app.
"""

# === Imports ===
import streamlit as st
from config.settings import cargar_configuracion
from utils.language_switch import leer_idioma
from ui.layout import (
    mostrar_mensaje_bienvenida,
    mostrar_aviso_logging,
    mostrar_boton_empezar,
    mostrar_input_pregunta,
    mostrar_respuesta_chat,
    mostrar_footer_aviso_logging
)
from agent.rag_agent import (
    cargar_chromadb,
    buscar_contexto_relevante,
    generar_respuesta
)
from logging.logger import guardar_logging

# === Load Configuration ===
CONFIG = cargar_configuracion()
COLLECTION_PATH = CONFIG["path_chromadb"]

# === Load Knowledge Base ===
collection = cargar_chromadb(COLLECTION_PATH)

# === Main App Function ===

def main() -> None:
    """Run the ItsMeHi Streamlit application."""
    st.set_page_config(page_title=CONFIG["proyecto_nombre_publico"], page_icon="👋", layout="centered")

    
    # Language selection
    idioma: str = leer_idioma()
    
    # Initialize session state
    if "chat_started" not in st.session_state:
        st.session_state["chat_started"] = False
    
    # === Welcome Screen ===
    if not st.session_state["chat_started"]:
        mostrar_mensaje_bienvenida(idioma)
        mostrar_aviso_logging(idioma)
        
        if mostrar_boton_empezar(idioma):
            st.session_state["chat_started"] = True
            st.experimental_rerun()
    
    # === Chatbot Screen ===
    else:
        pregunta: str = mostrar_input_pregunta(idioma)
        
        if pregunta:
            contexto: list[str] = buscar_contexto_relevante(pregunta, collection)
            respuesta: str = generar_respuesta(contexto, pregunta)
            
            mostrar_respuesta_chat(respuesta)
            guardar_logging(pregunta, respuesta)
    
    # === Footer ===
    mostrar_footer_aviso_logging()


# === Run Application ===
if __name__ == "__main__":
    main()
