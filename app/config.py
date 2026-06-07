# app/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# ─────────────────────────────────────────
# FIND .env FILE — Try multiple locations
# ─────────────────────────────────────────
# Get the directory where this config.py file lives
CURRENT_DIR = Path(__file__).resolve().parent

# Go UP one level (from app/ to project root)
PROJECT_ROOT = CURRENT_DIR.parent

# Possible .env locations
ENV_LOCATIONS = [
    PROJECT_ROOT / ".env",        # Most likely: project root
    CURRENT_DIR / ".env",         # Fallback: inside app folder
    Path.cwd() / ".env",          # Fallback: current working directory
]

# Try each location
env_loaded = False
for env_path in ENV_LOCATIONS:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"✅ Loaded .env from: {env_path}")
        env_loaded = True
        break

if not env_loaded:
    print("⚠️ WARNING: No .env file found in any location:")
    for path in ENV_LOCATIONS:
        print(f"   - {path}")

# ─────────────────────────────────────────
# GET API KEY — Try environment + Streamlit
# ─────────────────────────────────────────
def get_api_key():
    """Try to get API key from multiple sources."""

    # Source 1: Environment variable (from .env or system)
    key = os.getenv("WEATHER_API_KEY", "").strip()
    if key:
        print(f"✅ API Key found in environment (length: {len(key)})")
        return key

    # Source 2: Streamlit secrets (for Streamlit Cloud)
    try:
        import streamlit as st
        key = st.secrets.get("WEATHER_API_KEY", "").strip()
        if key:
            print(f"✅ API Key found in Streamlit secrets (length: {len(key)})")
            return key
    except Exception:
        pass

    print("❌ NO API KEY FOUND in any source")
    return ""


WEATHER_API_KEY = get_api_key()
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_TIMEOUT_SECONDS = 10

# ─────────────────────────────────────────
# FALLBACK DEFAULTS
# ─────────────────────────────────────────
FALLBACK_DEFAULTS = {
    "temperature": 25.0,
    "humidity": 60.0,
    "rainfall": 100.0,
    "N": 50,
    "P": 50,
    "K": 50,
    "ph": 6.5
}

# ─────────────────────────────────────────
# VALID RANGES
# ─────────────────────────────────────────
VALID_RANGES = {
    "temperature": (0.0, 50.0),
    "humidity": (0.0, 100.0),
    "rainfall": (0.0, 500.0),
    "N": (0, 140),
    "P": (5, 145),
    "K": (5, 205),
    "ph": (3.0, 10.0)
}