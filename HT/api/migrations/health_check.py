from flask import Blueprint, jsonify
import os, requests

health_bp = Blueprint('health', __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    status = {"api": "ok"}

    # Check HuggingFace
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if hf_token:
        try:
            r = requests.get("https://api-inference.huggingface.co/status/bert-base-uncased",
                             headers={"Authorization": f"Bearer {hf_token}"}, timeout=2)
            status["huggingface"] = "ok" if r.status_code == 200 else "degraded"
        except Exception:
            status["huggingface"] = "fail"
    else:
        status["huggingface"] = "missing"

    # Check NOAA stub
    status["noaa"] = "configured" if os.getenv("NOAA_API_KEY") else "missing"

    return jsonify(status)
