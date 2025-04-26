import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json
import streamlit as st
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

# === Constants ===
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_INFO = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
SHEET_ID = os.getenv("SHEET_ID")

# === Load credentials and connect to sheet ===
credentials = ServiceAccountCredentials.from_json_keyfile_dict(SERVICE_ACCOUNT_INFO, scopes=SCOPE)
client = gspread.authorize(credentials)

try:
    sheet = client.open_by_key(SHEET_ID).sheet1  # Open the first sheet
except Exception as e:
    st.error(f"⚡ Error connecting to Google Sheets: {e}")
    sheet = None  # Disable logging if connection fails

def log_to_google_sheet(pregunta: str, respuesta: str) -> None:
    """Append a new conversation entry to Google Sheets safely."""
    if sheet is None:
        # No sheet connected, skip logging
        print("⚡ Skipping logging: No connection to Google Sheets.")
        return

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fila = [fecha, pregunta, respuesta]

    try:
        sheet.append_row(fila)
        print(f"✅ Log saved to Google Sheets: {fila}")
    except Exception as e:
        st.error(f"⚡ Error saving log to Google Sheets: {e}")
