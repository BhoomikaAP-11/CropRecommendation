# app/api_handler.py

import requests
import logging
import os
from config import (
    WEATHER_API_KEY,
    WEATHER_BASE_URL,
    API_TIMEOUT_SECONDS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_weather_data(city_name: str) -> dict:
    """Fetch weather with FULL DEBUGGING."""

    # ─────────────────────────────────────
    # DEBUG: Print everything to terminal
    # ─────────────────────────────────────
    print("\n" + "="*60)
    print("🔍 WEATHER API DEBUG INFO")
    print("="*60)
    print(f"📍 City entered: '{city_name}'")
    print(f"🔑 API Key exists: {bool(WEATHER_API_KEY)}")
    print(f"🔑 API Key length: {len(WEATHER_API_KEY) if WEATHER_API_KEY else 0}")
    print(f"🔑 API Key (first 8 chars): {WEATHER_API_KEY[:8] if WEATHER_API_KEY else 'NONE'}...")
    print(f"🌐 Base URL: {WEATHER_BASE_URL}")
    print("="*60)

    # ─────────────────────────────────────
    # Check 1: API key exists
    # ─────────────────────────────────────
    if not WEATHER_API_KEY or WEATHER_API_KEY.strip() == "":
        print("❌ FAILURE REASON: API key is empty or missing")
        return {
            "success": False,
            "source": "manual_required",
            "data": None,
            "error_message": "⚠️ API key not found. Check your .env file."
        }

    # ─────────────────────────────────────
    # Check 2: City name provided
    # ─────────────────────────────────────
    if not city_name or city_name.strip() == "":
        print("❌ FAILURE REASON: City name is empty")
        return {
            "success": False,
            "source": "manual_required",
            "data": None,
            "error_message": "⚠️ Please enter a city name."
        }

    # ─────────────────────────────────────
    # Make API call
    # ─────────────────────────────────────
    try:
        params = {
            "q": city_name.strip(),
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        full_url = f"{WEATHER_BASE_URL}?q={city_name}&appid={WEATHER_API_KEY[:8]}...&units=metric"
        print(f"📡 Making request to: {full_url}")

        response = requests.get(
            WEATHER_BASE_URL,
            params=params,
            timeout=API_TIMEOUT_SECONDS
        )

        print(f"📥 Response status code: {response.status_code}")
        print(f"📥 Response text (first 200 chars): {response.text[:200]}")

        # ─────────────────────────────────
        # Handle different status codes
        # ─────────────────────────────────
        if response.status_code == 401:
            print("❌ FAILURE REASON: Invalid API key (401)")
            return {
                "success": False,
                "source": "manual_required",
                "data": None,
                "error_message": (
                    "❌ Invalid API key. "
                    "Wait 10 minutes after creating a new key (activation time). "
                    "Or check key spelling in .env file."
                )
            }

        if response.status_code == 404:
            print(f"❌ FAILURE REASON: City '{city_name}' not found (404)")
            return {
                "success": False,
                "source": "manual_required",
                "data": None,
                "error_message": f"❌ City '{city_name}' not found. Try a major city nearby."
            }

        if response.status_code == 429:
            print("❌ FAILURE REASON: Rate limit exceeded (429)")
            return {
                "success": False,
                "source": "manual_required",
                "data": None,
                "error_message": "⏳ Too many requests. Wait 1 minute."
            }

        if response.status_code != 200:
            print(f"❌ FAILURE REASON: Unexpected status {response.status_code}")
            return {
                "success": False,
                "source": "manual_required",
                "data": None,
                "error_message": f"❌ Service error: {response.status_code}"
            }

        # ─────────────────────────────────
        # SUCCESS!
        # ─────────────────────────────────
        data = response.json()
        print("✅ SUCCESS! Weather data received")
        print(f"   Temperature: {data['main']['temp']}°C")
        print(f"   Humidity: {data['main']['humidity']}%")
        print("="*60 + "\n")

        return {
            "success": True,
            "source": "api",
            "data": {
                "temperature": round(data["main"]["temp"], 1),
                "humidity": round(data["main"]["humidity"], 1),
                "description": data["weather"][0]["description"].title(),
                "city_confirmed": data["name"],
                "country": data["sys"]["country"]
            },
            "error_message": None
        }

    except requests.exceptions.ConnectionError as e:
        print(f"❌ FAILURE REASON: No internet connection — {e}")
        return {
            "success": False,
            "source": "manual_required",
            "data": None,
            "error_message": "📡 No internet connection."
        }

    except requests.exceptions.Timeout as e:
        print(f"❌ FAILURE REASON: Request timed out — {e}")
        return {
            "success": False,
            "source": "manual_required",
            "data": None,
            "error_message": "⏱️ Request timed out. Try again."
        }

    except Exception as e:
        print(f"❌ FAILURE REASON: Unknown error — {type(e).__name__}: {e}")
        return {
            "success": False,
            "source": "manual_required",
            "data": None,
            "error_message": f"❌ Error: {str(e)}"
        }