"""Configuration module for ItsMeHi App.

This module centralizes settings and constants used throughout the application.

Functions:
    cargar_configuracion(): Load and return the app configuration dictionary.
"""

# === Imports ===
from pathlib import Path

# === Functions ===

def cargar_configuracion() -> dict:
    """Load and return the application configuration dictionary.

    Returns:
        dict: Dictionary containing general app settings.
    """
    configuracion = {
        "proyecto_nombre_tecnico": "ItsMeHi",
        "proyecto_nombre_publico": "It's Me, Hi",
        "idioma_por_defecto": "es",
        "path_chromadb": Path("data/chromadb/"),  
        "path_logs": Path("logs/itsmehi_chat_logs.csv")
    }
    return configuracion
