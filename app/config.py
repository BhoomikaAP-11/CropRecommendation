# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────
# API CONFIGURATION
# ─────────────────────────────────────────
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_TIMEOUT_SECONDS = 5

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