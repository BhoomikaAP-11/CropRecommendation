# app/streamlit_app.py

import streamlit as st
import pandas as pd
import sys
import os

# Add app folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_handler import fetch_weather_data
from model_handler import load_crop_model, predict_crop
from config import FALLBACK_DEFAULTS, VALID_RANGES

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🌾 Smart Agriculture Advisor",
    page_icon="🌾",
    layout="wide"
)

# ─────────────────────────────────────────
# LOAD MODEL (cached)
# ─────────────────────────────────────────
@st.cache_resource
def get_model():
    return load_crop_model()

model_data = get_model()

# ─────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────
def init_session_state():
    defaults = {
        "temperature": FALLBACK_DEFAULTS["temperature"],
        "humidity": FALLBACK_DEFAULTS["humidity"],
        "rainfall": FALLBACK_DEFAULTS["rainfall"],
        "N": FALLBACK_DEFAULTS["N"],
        "P": FALLBACK_DEFAULTS["P"],
        "K": FALLBACK_DEFAULTS["K"],
        "ph": FALLBACK_DEFAULTS["ph"],
        "weather_source": "manual",
        "api_fetch_done": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("🌾 Crop Recommendation & Smart Agriculture Advisor")
st.markdown("*AI-powered decision support system*")
st.markdown("---")

# ─────────────────────────────────────────
# SECTION 1: WEATHER
# ─────────────────────────────────────────
st.header("🌤️ Step 1: Weather Conditions")

col_city, col_btn = st.columns([3, 1])
with col_city:
    city_input = st.text_input("Enter your city:",
                                 placeholder="e.g. Pune, Lucknow")
with col_btn:
    st.write("")
    st.write("")
    fetch_clicked = st.button("📡 Fetch Weather", use_container_width=True)

if fetch_clicked:
    if not city_input.strip():
        st.warning("⚠️ Please enter a city name.")
    else:
        with st.spinner(f"Fetching weather for {city_input}..."):
            result = fetch_weather_data(city_input)

        if result["success"]:
            data = result["data"]
            st.session_state["temperature"] = data["temperature"]
            st.session_state["humidity"] = data["humidity"]
            st.session_state["weather_source"] = "api"
            st.session_state["api_fetch_done"] = True
            st.success(
                f"✅ Weather fetched for **{data['city_confirmed']}, "
                f"{data['country']}** — {data['description']}"
            )
        else:
            st.session_state["weather_source"] = "manual"
            st.session_state["api_fetch_done"] = True
            st.error(result["error_message"])

# Weather inputs (always shown, always editable)
st.markdown("#### Weather Parameters")
st.caption("💡 *Adjust these to match your actual field conditions*")

col1, col2, col3 = st.columns(3)
with col1:
    temperature = st.slider(
        "🌡️ Temperature (°C)",
        VALID_RANGES["temperature"][0], VALID_RANGES["temperature"][1],
        float(st.session_state["temperature"]), 0.5
    )
    st.session_state["temperature"] = temperature

with col2:
    humidity = st.slider(
        "💧 Humidity (%)",
        VALID_RANGES["humidity"][0], VALID_RANGES["humidity"][1],
        float(st.session_state["humidity"]), 0.5
    )
    st.session_state["humidity"] = humidity

with col3:
    rainfall = st.slider(
        "🌧️ Rainfall (mm)",
        VALID_RANGES["rainfall"][0], VALID_RANGES["rainfall"][1],
        float(st.session_state["rainfall"]), 1.0
    )
    st.session_state["rainfall"] = rainfall

st.markdown("---")

# ─────────────────────────────────────────
# SECTION 2: SOIL DATA
# ─────────────────────────────────────────
st.header("🧪 Step 2: Soil Nutrient Levels")
st.info(
    "💡 Get soil test report from your nearest Krishi Kendra "
    "or use a soil testing kit."
)

col1, col2 = st.columns(2)
with col1:
    N = st.number_input(
        "🟡 Nitrogen (N) kg/ha",
        VALID_RANGES["N"][0], VALID_RANGES["N"][1],
        st.session_state["N"], 1
    )
    st.session_state["N"] = N

    P = st.number_input(
        "🟠 Phosphorus (P) kg/ha",
        VALID_RANGES["P"][0], VALID_RANGES["P"][1],
        st.session_state["P"], 1
    )
    st.session_state["P"] = P

    K = st.number_input(
        "🟣 Potassium (K) kg/ha",
        VALID_RANGES["K"][0], VALID_RANGES["K"][1],
        st.session_state["K"], 1
    )
    st.session_state["K"] = K

with col2:
    ph = st.slider(
        "⚗️ Soil pH",
        VALID_RANGES["ph"][0], VALID_RANGES["ph"][1],
        float(st.session_state["ph"]), 0.1
    )
    st.session_state["ph"] = ph

    if ph < 5.5:
        st.error(f"pH {ph} — Strongly Acidic")
    elif ph < 6.5:
        st.warning(f"pH {ph} — Slightly Acidic")
    elif ph <= 7.5:
        st.success(f"pH {ph} — Neutral (Ideal)")
    elif ph <= 8.5:
        st.warning(f"pH {ph} — Slightly Alkaline")
    else:
        st.error(f"pH {ph} — Strongly Alkaline")

st.markdown("---")

# ─────────────────────────────────────────
# SECTION 3: PREDICT
# ─────────────────────────────────────────
if st.button("🌱 Get Crop Recommendation", use_container_width=True,
              type="primary"):
    if not model_data["success"]:
        st.error(f"❌ Model not loaded: {model_data['error']}")
    else:
        input_values = {
            "N": st.session_state["N"],
            "P": st.session_state["P"],
            "K": st.session_state["K"],
            "temperature": st.session_state["temperature"],
            "humidity": st.session_state["humidity"],
            "ph": st.session_state["ph"],
            "rainfall": st.session_state["rainfall"]
        }

        with st.spinner("🔄 Analysing..."):
            result = predict_crop(
                model_data["model"],
                model_data["scaler"],
                model_data["label_encoder"],
                input_values
            )

        if result["success"]:
            st.balloons()
            st.success(f"## 🌾 Recommended Crop: **{result['recommended_crop'].upper()}**")
            st.metric("Confidence", f"{result['confidence']}%")

            st.subheader("📊 Top 3 Suggestions:")
            for i, item in enumerate(result["top3"]):
                emoji = ["🥇", "🥈", "🥉"][i]
                st.write(f"{emoji} **{item['crop'].capitalize()}** — {item['confidence']}%")
                st.progress(item["confidence"] / 100)
        else:
            st.error(f"❌ Prediction failed: {result['error']}")

st.markdown("---")
st.caption("🌾 Smart Agriculture Advisor | Disclaimer: For advisory purposes only.")