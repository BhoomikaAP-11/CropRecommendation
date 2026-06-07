# app/api_handler.py

import requests
import logging
from config import (
    WEATHER_API_KEY,
    WEATHER_BASE_URL,
    API_TIMEOUT_SECONDS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_weather_data(city_name: str) -> dict:
    """Fetch weather with full error handling and fallback."""

    if not WEATHER_API_KEY:
        return {
            "success": False,
            "source": "manual_required",
            "data": None,
            "error_message": "⚠️ Weather API not configured. Enter values manually."
        }

    if not city_name or city_name.strip() == "":
        return {
            "success": False,
            "source": "manual_required",
            "data": None,
            "error_message": "⚠️ Please enter a city name."
        }

    try:
        params = {
            "q": city_name.strip(),
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(WEATHER_BASE_URL, params=params,
                                  timeout=API_TIMEOUT_SECONDS)

        if response.status_code == 401:
            return {"success": False, "source": "manual_required",
                    "data": None,
                    "error_message": "❌ Invalid API key. Enter values manually."}

        if response.status_code == 404:
            return {"success": False, "source": "manual_required",
                    "data": None,
                    "error_message": f"❌ City '{city_name}' not found."}

        if response.status_code == 429:
            return {"success": False, "source": "manual_required",
                    "data": None,
                    "error_message": "⏳ API rate limit reached. Enter manually."}

        if response.status_code != 200:
            return {"success": False, "source": "manual_required",
                    "data": None,
                    "error_message": f"❌ Service error {response.status_code}."}

        data = response.json()

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

    except requests.exceptions.ConnectionError:
        return {"success": False, "source": "manual_required",
                "data": None,
                "error_message": "📡 No internet. Enter values manually."}

    except requests.exceptions.Timeout:
        return {"success": False, "source": "manual_required",
                "data": None,
                "error_message": "⏱️ Request timed out. Enter values manually."}

    except Exception as e:
        logger.error(f"Unknown error: {e}")
        return {"success": False, "source": "manual_required",
                "data": None,
                "error_message": "❌ Something went wrong. Enter values manually."}