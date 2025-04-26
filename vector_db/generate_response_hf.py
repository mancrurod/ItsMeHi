import os
import logging
from typing import List

from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

# === Initialize Hugging Face Inference Client ===
hf_token = os.getenv("HF_TOKEN")
client = InferenceClient(token=hf_token)

# === Constants ===
MAX_TOKENS = 500

# === Initialize logger ===
logger = logging.getLogger(__name__)


def generate_response_hf(context: List[str], question: str) -> str:
    """Generates a response using a Hugging Face model.

    Args:
        context (List[str]): List of relevant context paragraphs.
        question (str): User's question.

    Returns:
        str: Generated answer.
    """
    # Merge context into a single string
    context_combined = "\n".join(context)

    # Build prompt
    prompt = (
        f"Use the following context to answer clearly and professionally.\n\n"
        f"Context:\n\n{context_combined}\n\n"
        f"Question:\n{question}\n\n"
        f"Answer:"
    )

    # Debug log: first 100 characters of the prompt
    logger.debug(f"🚀 Sending prompt to HuggingFace (first 100 chars): {prompt[:100]}")

    try:
        # Send request to Hugging Face Inference API
        response = client.text_generation(
            model="tiiuae/falcon-7b-instruct",
            prompt=prompt,
            max_new_tokens=MAX_TOKENS,
            temperature=0.5,
        )

        # Extract and return the generated text
        return response.generated_text.strip()

    except Exception as e:
        logger.error(f"⚡ Real error captured:\n\n{e}")
        return "⚡ The model did not respond or took too long. Please try again later."
