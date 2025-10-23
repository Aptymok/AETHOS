import numpy as np
from flask import Blueprint, jsonify, request
from models import db, Manifest, User
from auth import require_jwt
from core.agents import create_agent_mask
from integrations.huggingface import analyze_narrative
from core.metrics import compute_entropy, compute_alignment, compute_manifestation_progress
from sockets.events import emit_resonance_update

manifest_bp = Blueprint('manifest', __name__)

@manifest_bp.route('/manifest', methods=['POST'])
@require_jwt
def create_manifestation():
    try:
        data = request.get_json()
        user_id = request.user['id']
        intention = data.get('intention', '').strip()
        mask_name = data.get('mask', 'Narrador')
        session_context = data.get('context', {})
        
        if not intention:
            return jsonify({'error': 'IntenciÃ³n vacÃ­a'}), 400
        
        # 1. AnÃ¡lisis narrativo avanzado
        analysis = analyze_narrative(intention)
        
        # 2. Obtener historial del usuario para mÃ©tricas contextuales
        user_history = get_user_manifestation_history(user_id)
        user_profile = get_user_profile(user_id)
        
        # 3. Calcular mÃ©tricas avanzadas
        entropy = compute_entropy(analysis, user_history)
        alignment = compute_alignment(intention, analysis, user_profile)
        
        # 4. Crear agente segÃºn mÃ¡scara seleccionada
        agent = create_agent_mask(mask_name)
        
        # 5. Generar respuesta contextualizada
        user_metrics = {'entropy': entropy, 'alignment': alignment}
        agent_response = agent.respond(intention, analysis, user_metrics)
        
        # 6. Calcular progreso de manifestaciÃ³n
        session_data = {
            'current_entropy': entropy,
            'current_alignment': alignment,
            'interactions': user_history[-3:] if user_history else [],
            'cluster_strength': analysis['resonance_score']
        }
        manifestation_progress = compute_manifestation_progress(user_id, session_data)
        
        # 7. Guardar en base de datos
        manifest = Manifest(
            user_id=user_id,
            intention=intention,
            mask=mask_name,
            entropy=entropy,
            alignment=alignment,
            keywords=','.join(analysis['keywords']),
            cluster=analysis['cluster'],
            resonance_score=analysis['resonance_score'],
            progress=manifestation_progress
        )
        db.session.add(manifest)
        db.session.commit()
        
        # 8. Actualizar mÃ©tricas del usuario
        update_user_coherence(user_id, alignment, entropy)
        
        # 9. Emitir actualizaciÃ³n de resonancia
        resonance_data = {
            'user_id': user_id,
            'cluster': analysis['cluster'],
            'entropy': entropy,
            'alignment': alignment,
            'progress': manifestation_progress,
            'timestamp': manifest.created_at.isoformat()
        }
        emit_resonance_update(analysis['cluster'], resonance_data)
        
        # 10. Preparar respuesta completa
        response = {
            'manifest_id': manifest.id,
            'narration': agent_response,
            'metrics': {
                'entropy': entropy,
                'alignment': alignment,
                'manifestation_progress': manifestation_progress,
                'clearing_percentage': calculate_clearing_percentage(user_history, entropy) if user_history else 0,
                'cluster': analysis['cluster'],
                'resonance': analysis['resonance_score'],
                'semantic_depth': analysis['semantic_depth']
            },
            'context': {
                'keywords': analysis['keywords'],
                'recommended_masks': suggest_alternative_masks(mask_name, analysis),
                'next_steps': generate_next_steps(manifestation_progress, entropy)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error en manifestaciÃ³n: {str(e)}'}), 500

def get_user_manifestation_history(user_id):
    """Obtiene historial reciente de manifestaciones del usuario"""
    manifests = Manifest.query.filter_by(user_id=user_id)\
        .order_by(Manifest.created_at.desc())\
        .limit(10)\
        .all()
    return [{'entropy': m.entropy, 'alignment': m.alignment} for m in manifests]

def get_user_profile(user_id):
    """Obtiene perfil del usuario para personalizaciÃ³n"""
    user = User.query.get(user_id)
    if user:
        recent_manifests = Manifest.query.filter_by(user_id=user_id)\
            .order_by(Manifest.created_at.desc())\
            .limit(5)\
            .all()
        avg_alignment = np.mean([m.alignment for m in recent_manifests]) if recent_manifests else 0.5
        return {'avg_alignment': avg_alignment, 'coherence': user.coherence}
    return {}

def update_user_coherence(user_id, alignment, entropy):
    """Actualiza coherencia del usuario basada en manifestaciones"""
    user = User.query.get(user_id)
    if user:
        # Coherencia como balance entre alineamiento y baja entropÃ­a
        new_coherence = (alignment + (1 - entropy)) / 2
        user.coherence = max(0.1, min(0.99, new_coherence))
        db.session.commit()

def calculate_clearing_percentage(history, current_entropy):
    """Calcula porcentaje de limpieza basado en reducciÃ³n de entropÃ­a"""
    if not history:
        return 0.0
    
    initial_entropy = history[0]['entropy'] if history else 0.5
    entropy_reduction = initial_entropy - current_entropy
    clearing = (entropy_reduction / initial_entropy) * 100 if initial_entropy > 0 else 0
    return round(max(0, min(100, clearing)), 1)

def suggest_alternative_masks(current_mask, analysis):
    """Sugiere mÃ¡scaras alternativas basadas en el anÃ¡lisis"""
    suggestions = {
        'Narrador': ['Arquitecto', 'Visionario'],
        'Arquitecto': ['Ingeniero', 'Narrador'],
        'Visionario': ['OrÃ¡culo', 'Sombra'],
        'Sombra': ['Narrador', 'Arquitecto'],
        'OrÃ¡culo': ['Visionario', 'Narrador'],
        'Ingeniero': ['Arquitecto', 'Narrador']
    }
    
    # Ajustar sugerencias basadas en clÃºster
    cluster_adjustments = {
        'AETHOS': ['Arquitecto', 'Ingeniero'],
        'TRANSFORMACIÃ“N': ['Sombra', 'Visionario'],
        'VÃNCULO': ['Narrador', 'OrÃ¡culo']
    }
    
    base_suggestions = suggestions.get(current_mask, ['Narrador', 'Arquitecto'])
    cluster_suggestions = cluster_adjustments.get(analysis['cluster'], [])
    
    return list(set(base_suggestions + cluster_suggestions))[:3]

def generate_next_steps(progress, entropy):
    """Genera prÃ³ximos pasos basados en progreso y estado actual"""
    if progress < 0.3:
        return [
            "Refina tu intenciÃ³n - hazla mÃ¡s especÃ­fica",
            "Realiza una tirada de cartas para clarificar",
            "Consulta con la mÃ¡scara 'Sombra' para identificar bloqueos"
        ]
    elif progress < 0.7:
        return [
            "Profundiza en el clÃºster actual con otra manifestaciÃ³n",
            "Experimenta con una mÃ¡scara diferente",
            "Observa patrones resonantes en la LegiÃ³n"
        ]
    else:
        return [
            "Consolida los insights en un protocolo ejecutable",
            "Comparte tu proceso con la LegiÃ³n",
            "DiseÃ±a la siguiente iteraciÃ³n de tu manifestaciÃ³n"
        ]

