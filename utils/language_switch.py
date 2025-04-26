"""Language switcher module for ItsMeHi.

This module handles the language selection functionality,
allowing users to switch dynamically between Spanish and English.

Functions:
    leer_idioma(): Display the language selector and return the selected language code.
"""

# === Imports ===
import streamlit as st
from config.settings import cargar_configuracion

# === Functions ===

def leer_idioma() -> str:
    """Display the language selector and return the selected language code.

    Returns:
        str: 'es' for Spanish or 'en' for English.
    """
    config = cargar_configuracion()
    idioma_por_defecto = config["idioma_por_defecto"]
    
    if "idioma" not in st.session_state:
        st.session_state["idioma"] = idioma_por_defecto

    idioma_previo = st.session_state["idioma"]

    idioma_seleccionado = st.radio(
        "🌐 Select language:",
        options=["Español", "English"],
        index=0 if idioma_previo == "es" else 1,
        horizontal=True
    )

    nuevo_idioma = "es" if idioma_seleccionado == "Español" else "en"

    if nuevo_idioma != idioma_previo:
        st.session_state["idioma"] = nuevo_idioma
        st.rerun()  # 🔥 Aquí forzamos el rerun instantáneo cuando cambia

    return st.session_state["idioma"]
