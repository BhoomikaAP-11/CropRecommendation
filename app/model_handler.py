# app/model_handler.py

import pickle
import numpy as np
import logging

logger = logging.getLogger(__name__)


def load_crop_model():
    """Load model, scaler, and label encoder."""
    try:
        with open("models/crop_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("models/scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        with open("models/label_encoder.pkl", "rb") as f:
            label_encoder = pickle.load(f)

        return {
            "success": True,
            "model": model,
            "scaler": scaler,
            "label_encoder": label_encoder
        }
    except FileNotFoundError as e:
        return {"success": False, "error": f"File not found: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def predict_crop(model, scaler, label_encoder, input_values: dict) -> dict:
    """Predict crop from input values."""
    try:
        features = np.array([[
            input_values["N"],
            input_values["P"],
            input_values["K"],
            input_values["temperature"],
            input_values["humidity"],
            input_values["ph"],
            input_values["rainfall"]
        ]])

        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)
        probabilities = model.predict_proba(features_scaled)[0]

        crop_name = label_encoder.inverse_transform(prediction)[0]

        top3_idx = np.argsort(probabilities)[-3:][::-1]
        top3 = [
            {
                "crop": label_encoder.inverse_transform([idx])[0],
                "confidence": round(probabilities[idx] * 100, 2)
            }
            for idx in top3_idx
        ]

        return {
            "success": True,
            "recommended_crop": crop_name,
            "confidence": round(np.max(probabilities) * 100, 2),
            "top3": top3
        }
    except Exception as e:
        return {"success": False, "error": str(e)}