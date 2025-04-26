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
    return st.text_input(TEXTOS["input_pregunta"][idioma])


def mostrar_respuesta_chat(respuesta: str) -> None:
    """Display the chatbot's generated response."""
    st.write(respuesta)


def mostrar_footer_aviso_logging() -> None:
    """Display a small footer reminding about conversation logging."""
    st.markdown(
        """
        <small>⚙️ Este chat puede ser registrado para mejorar el servicio. / This chat may be recorded to improve the service.</small>
        """, unsafe_allow_html=True
    )
