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
    mostrar_footer_aviso_logging,
    mostrar_mensaje_recruiter,
    mostrar_mensaje_bot
)
from agent.rag_agent import (
    cargar_qdrant,
    buscar_contexto_relevante,
    generar_respuesta
)
from vector_db.log_to_google_sheet import log_to_google_sheet

# === Load Configuration ===
CONFIG = cargar_configuracion()

# === Load Knowledge Base ===
qdrant_client = cargar_qdrant()

# === Initialize Session State ===
if "chat_started" not in st.session_state:
    st.session_state["chat_started"] = False
if "historial_chat" not in st.session_state:
    st.session_state["historial_chat"] = []
if "input_ready" not in st.session_state:
    st.session_state["input_ready"] = False
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""
if "new_question" not in st.session_state:
    st.session_state["new_question"] = ""

# === Function to handle input submission ===
def submit_question() -> None:
    """Handle the submission of a new question."""
    if st.session_state["new_question"].strip() != "":
        st.session_state["input_text"] = st.session_state["new_question"]
        st.session_state["input_ready"] = True

# === Main Application ===

def main() -> None:
    """Run the ItsMeHi Streamlit application."""
    st.set_page_config(page_title=CONFIG["proyecto_nombre_publico"], page_icon="👋", layout="centered")
    
    idioma: str = leer_idioma()

    # === Welcome Screen ===
    if not st.session_state["chat_started"]:
        mostrar_mensaje_bienvenida(idioma)
        mostrar_aviso_logging(idioma)

        if mostrar_boton_empezar(idioma):
            st.session_state["chat_started"] = True
            st.rerun()

    # === Chatbot Screen ===
    else:
        # Button to go back to the welcome screen
        if st.button("⬅️"):
            st.session_state["chat_started"] = False
            st.session_state["historial_chat"] = []
            st.session_state["input_ready"] = False
            st.session_state["input_text"] = ""
            st.session_state["new_question"] = ""
            st.rerun()

        # Display chat history
        for pregunta_antigua, respuesta_antigua in st.session_state["historial_chat"]:
            mostrar_mensaje_recruiter(pregunta_antigua)
            mostrar_mensaje_bot(respuesta_antigua)

        # New question input with Enter key submission
        if not st.session_state.get("input_ready", False):
            st.text_input(
                label="Pregunta",
                placeholder="¿Sobre qué quieres preguntarme? 🚀",
                label_visibility="collapsed",
                key="new_question",
                on_change=submit_question
            )
            
            # Now show the footer info AFTER the input
            mostrar_footer_aviso_logging()

        # Process the question only if ready
        if st.session_state["input_ready"]:
            thinking_placeholder = st.empty()
            thinking_placeholder.info("🤖 Pensando...")

        try:
            contexto = buscar_contexto_relevante(st.session_state["input_text"], qdrant_client)
            respuesta = generar_respuesta(contexto, st.session_state["input_text"])
        except Exception as e:
            respuesta = "⚠️ Ha ocurrido un error al generar la respuesta. Inténtalo más tarde."
            st.error(f"❌ Error técnico: {e}")

            thinking_placeholder.empty()

            st.session_state["historial_chat"].append((st.session_state["input_text"], respuesta))
            try:
                log_to_google_sheet(st.session_state["input_text"], respuesta)
            except Exception as e:
                st.warning(f"⚠️ No se pudo registrar la conversación en Sheets: {e}")
                
            # Reset states after processing
            st.session_state["input_text"] = ""
            st.session_state["input_ready"] = False

            # Success and info messages
            st.success("✅ Pregunta enviada correctamente!")
            st.info("🚦 Por favor, espere unos segundos antes de enviar otra pregunta.")

            st.rerun()

# === Run Application ===
if __name__ == "__main__":
    main()
