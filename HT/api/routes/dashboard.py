from flask import Blueprint, jsonify
import random

dashboard_bp = Blueprint('dashboard', __name__)


def compute_entropy(analysis):
    return round(random.uniform(0.15,0.9),2)


def compute_alignment(intention, analysis):
    return round(max(0.0, 1 - compute_entropy(analysis) * random.uniform(0.5,1.0)), 2)


@dashboard_bp.route('/dashboard/metrics', methods=['GET'])
def get_metrics():
    # endpoint de ejemplo que devuelve métricas simuladas
    return jsonify({
        'entropy': compute_entropy({}),
        'alignment': compute_alignment('', {})
    })
