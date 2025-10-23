from flask import Blueprint, jsonify, request
import os

admin_bp = Blueprint("admin", __name__)
SYSTEM_STATE = {"active": True}

@admin_bp.route("/ops/pause-all", methods=["POST"])
def pause_all():
    token = request.headers.get("X-ADMIN-TOKEN")
    if token != os.getenv("ADMIN_TOKEN"):
        return jsonify({"error": "unauthorized"}), 401

    SYSTEM_STATE["active"] = False
    return jsonify({"status": "paused", "message": "all resonance processes halted"}), 200

@admin_bp.route("/ops/status", methods=["GET"])
def system_status():
    return jsonify(SYSTEM_STATE)
