import os
import logging
from typing import List

from huggingface_hub import InferenceClient

# === Configure Logging ===
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# === Load Environment Variables ===
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# === Initialize Hugging Face Client ===
client = InferenceClient(token=HUGGINGFACE_API_TOKEN)

# === Constants ===
MODEL_NAME = "tiiuae/falcon-7b-instruct"
MAX_OUTPUT_TOKENS = 200  # Falcon models are relatively large, keep response small


def generar_respuesta_hf(contexto: List[str], pregunta: str) -> str:
    """
    Generate a response using Hugging Face Inference API (tiiuae/falcon-7b-instruct).

    Args:
        contexto (List[str]): List of context passages.
        pregunta (str): User's question.

    Returns:
        str: Generated answer from the model.
    """
    contexto_unido = "\n".join(contexto)

    prompt = (
        f"Use the following information to answer clearly and professionally.\n\n"
        f"Context:\n{contexto_unido}\n\n"
        f"Question:\n{pregunta}\n"
    )

    try:
        logger.debug(f"\U0001F680 Sending prompt to HuggingFace (first 100 chars): {prompt[:100]}")

        response = client.text_generation(
            prompt,
            model=MODEL_NAME,
            max_new_tokens=MAX_OUTPUT_TOKENS,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )

        return response.strip()

    except Exception as e:
        logger.error(f"⚡ Real error captured:\n{e}")
        return "⚡ The model did not respond or took too long. Please try again later."