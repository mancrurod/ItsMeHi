"""UI Components for ItsMeHi App.

This module handles the visual components and user interactions for the ItsMeHi Streamlit application.

Functions:
    mostrar_mensaje_bienvenida(idioma): Display the welcome message based on the selected language.
    mostrar_aviso_logging(idioma): Show the logging notice banner.
    mostrar_boton_empezar(idioma): Display the 'Start Chat' button and return its state.
    mostrar_input_pregunta(idioma): Display the input box for recruiter questions.
    mostrar_respuesta_chat(respuesta): Display the chatbot's answer.
    mostrar_footer_aviso_logging(): Show a small footer reminding about logging.
"""

# === Imports ===
import streamlit as st
from ui.texts import TEXTOS
from config.settings import cargar_configuracion

CONFIG = cargar_configuracion()
NOMBRE_BOT = CONFIG["nombre_bot"]

# === Functions ===

def mostrar_mensaje_bienvenida(idioma: str) -> None:
    """Display the welcome message in the selected language."""
    st.title(TEXTOS["bienvenida_titulo"][idioma])
    st.write(TEXTOS["bienvenida_descripcion"][idioma])


def mostrar_aviso_logging(idioma: str) -> None:
    """Display the logging notice banner."""
    st.warning(TEXTOS["aviso_logging_banner"][idioma])


def mostrar_boton_empezar(idioma: str) -> bool:
    """Display the 'Start Chat' button and return True if clicked."""
    return st.button(TEXTOS["boton_empezar"][idioma])


def mostrar_input_pregunta(idioma: str) -> str:
    """Display the input box for recruiter questions and return the user's input."""
    placeholder_text = {
        "es": "¿Qué te gustaría saber de mí? 🤓",
        "en": "What would you like to know about me? 🤓"
    }
    return st.text_input(
        label="Pregunta",
        placeholder=placeholder_text[idioma],
        label_visibility="collapsed"
    )

def mostrar_respuesta_chat(respuesta: str) -> None:
    """Display the chatbot's generated response."""
    st.write(respuesta)

def mostrar_footer_aviso_logging() -> None:
    """Display a small footer notice about chat logging."""
    st.markdown(
        """
        <div style="text-align: center; font-size: 0.75rem; color: #6c757d; margin-top: 10px;">
            ⚙️ Este chat puede ser registrado para mejorar el servicio. / This chat may be recorded to improve the service.
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_mensaje_recruiter(mensaje: str) -> None:
    """Display the recruiter's message in a styled chat bubble."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            padding: 12px;
            border-radius: 15px 15px 0px 15px;
            margin: 10px 0;
            max-width: 70%;
            float: right;
            clear: both;
            ">
            <b>🧑‍💼 Tú:</b> {mensaje}
        </div>
        """,
        unsafe_allow_html=True
    )

def mostrar_mensaje_bot(mensaje: str) -> None:
    """Display the bot's message in a styled chat bubble."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 12px;
            border-radius: 15px 15px 15px 0px;
            margin: 10px 0;
            max-width: 70%;
            float: left;
            clear: both;
            ">
            <b>🤖 {NOMBRE_BOT}:</b> {mensaje}
        </div>
        """,
        unsafe_allow_html=True
    )

def mostrar_input_pregunta(idioma: str) -> str:
    """Display the input box for recruiter questions with autofocus and return the user's input."""
    placeholder_text = {
        "es": "¿Sobre qué quieres preguntarme? 🚀",
        "en": "What would you like to ask me about? 🚀"
    }
    
    # Normal input
    input_value = st.text_input(
        label="Pregunta",
        placeholder=placeholder_text[idioma],
        label_visibility="collapsed",
        key="input_chat"
    )
    
    # Script for autofocus
    st.markdown(
        """
        <script>
        const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
        if (input) {input.focus();}
        </script>
        """,
        unsafe_allow_html=True
    )
    
    return input_value

