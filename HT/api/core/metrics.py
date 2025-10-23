import numpy as np
from datetime import datetime, timedelta

def compute_entropy(analysis, user_history=None):
    """Calcula entropía basada en dispersión semántica y coherencia histórica"""
    base_entropy = len(analysis['keywords']) / 10  # Más keywords → más entropía
    depth_factor = 1 - analysis['semantic_depth']  # Menos profundidad → más entropía
    
    # Factor histórico si hay datos previos
    history_factor = 1.0
    if user_history:
        recent_entropy = np.mean([h.get('entropy', 0.5) for h in user_history[-5:]])
        history_factor = 0.3 + abs(0.5 - recent_entropy) * 1.4
    
    entropy = min(0.95, max(0.05, base_entropy * depth_factor * history_factor))
    return round(entropy, 3)

def compute_alignment(intention, analysis, user_profile=None):
    """Calcula alineamiento entre intención y patrones resonantes"""
    # Alineamiento basado en coherencia de clúster
    cluster_strength = analysis['resonance_score']
    
    # Factor de longitud (intenciones más específicas tienden a mejor alineamiento)
    length_factor = min(1.0, len(intention) / 100)
    
    # Factor de profundidad semántica
    depth_factor = analysis['semantic_depth']
    
    # Ajuste basado en perfil histórico del usuario
    profile_factor = 1.0
    if user_profile and 'avg_alignment' in user_profile:
        profile_factor = 0.7 + (user_profile['avg_alignment'] * 0.3)
    
    alignment = cluster_strength * depth_factor * length_factor * profile_factor
    return round(max(0.1, min(0.99, alignment)), 3)

def compute_manifestation_progress(user_id, session_data):
    """Calcula progreso de manifestación basado en múltiples factores"""
    factors = {
        'entropy_reduction': max(0, 0.5 - session_data.get('current_entropy', 0.5)),
        'alignment_increase': max(0, session_data.get('current_alignment', 0.3) - 0.3),
        'session_depth': len(session_data.get('interactions', [])) / 10,
        'cluster_resonance': session_data.get('cluster_strength', 0.5),
        'temporal_consistency': calculate_temporal_consistency(user_id)
    }
    
    progress = sum(factors.values()) / len(factors)
    return round(max(0, min(1.0, progress)), 3)

def calculate_temporal_consistency(user_id):
    """Calcula consistencia temporal basada en historial de uso"""
    # En implementación real, consultaría la base de datos
    return np.random.uniform(0.3, 0.8)

def calculate_clearing_percentage(entropy_history, alignment_history):
    """Calcula porcentaje de limpieza basado en reducción de entropía"""
    if len(entropy_history) < 2:
        return 0.0
    
    initial_entropy = entropy_history[0]
    current_entropy = entropy_history[-1]
    entropy_reduction = initial_entropy - current_entropy
    
    clearing = (entropy_reduction / initial_entropy) * 100 if initial_entropy > 0 else 0
    return round(max(0, min(100, clearing)), 1)