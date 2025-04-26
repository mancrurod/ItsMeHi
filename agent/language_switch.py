"""Language switcher module for ItsMeHi.

This module handles the language toggle functionality,
allowing users to switch dynamically between Spanish and English.

Functions:
    leer_idioma(): Display the language toggle and return the selected language code.
"""

# === Imports ===
import streamlit as st
from config.settings import cargar_configuracion

# === Functions ===

def leer_idioma() -> str:
    """Display the language toggle and return the selected language code.

    Returns:
        str: 'es' for Spanish or 'en' for English.
    """
    config = cargar_configuracion()
    idioma_por_defecto = config["idioma_por_defecto"]
    
    # Initialize session state for language if not set
    if "idioma" not in st.session_state:
        st.session_state["idioma"] = idioma_por_defecto

    # Display language toggle
    idioma_seleccionado = st.toggle(
        label="🌐 Cambiar idioma / Switch language",
        value=True if st.session_state["idioma"] == "en" else False
    )
    
    # Update session state based on toggle position
    st.session_state["idioma"] = "en" if idioma_seleccionado else "es"
    
    return st.session_state["idioma"]
