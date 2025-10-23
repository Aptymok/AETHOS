from flask import Blueprint, jsonify
import os, requests

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    status = {"api": "ok"}
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    status["huggingface"] = "present" if hf_token else "missing"
    status["noaa"] = "configured" if os.getenv("NOAA_API_KEY") else "missing"
    return jsonify(status)
