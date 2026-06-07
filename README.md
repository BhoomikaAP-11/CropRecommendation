# 🌾 Crop Recommendation & Smart Agriculture Advisor

ML-powered crop recommendation system with weather API integration.

## Features
- 🌱 Recommends optimal crop from 22 options
- 📡 Real-time weather data with manual fallback
- 🧪 Soil nutrient analysis
- 📊 99%+ model accuracy

## Tech Stack
Python | Scikit-learn | XGBoost | Streamlit | OpenWeatherMap API

## Setup
```bash
git clone <your-repo-url>
cd crop-advisor
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py