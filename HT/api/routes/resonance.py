from flask import Blueprint, jsonify, current_app
import os
from core.resonance import ExternalResonanceEngine

resonance_bp = Blueprint('resonance', __name__)
resonance_engine = ExternalResonanceEngine()


@resonance_bp.route('/external', methods=['GET'])
async def get_external_resonance():
    """Obtiene datos de resonancia externa en tiempo real"""
    try:
        resonance_data = await resonance_engine.fetch_global_resonance()
        return jsonify(resonance_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@resonance_bp.route('/neural', methods=['GET'])
def get_neural_network_data():
    """Obtiene datos para el mapa neural.

    En staging/dev este endpoint puede devolver datos simulados cuando
    SIMULATE=true. En producción debe integrarse con la base de datos.
    """
    simulate = os.getenv('SIMULATE', 'true').lower() == 'true'
    if not simulate:
        return jsonify({'error': 'Simulations disabled. Integrate DB source for neural map.'}), 503

    # Modo simulado (determinista)
    simulated_data = {
        'nodes': [],
        'connections': [],
        'collective_coherence': 0.75,
        'active_clusters': ['AETHOS', 'TRANSFORMACIÓN', 'VÍNCULO']
    }
    return jsonify(simulated_data)