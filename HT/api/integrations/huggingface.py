import os
import requests
import numpy as np
from datetime import datetime

HF_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models"

def generate_text(prompt, model="microsoft/DialoGPT-large", max_tokens=200):
    """Generación de texto con modelos más avanzados"""
    if not HF_TOKEN:
        # Fallback determinista en staging: no dependemos de aleatoriedad
        return f"[SIMULATED] {prompt[:100]}... [Configure HUGGINGFACE_TOKEN para respuestas reales]"
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.85,
            "top_p": 0.95,
            "repetition_penalty": 1.2
        },
        "options": {"wait_for_model": True}
    }
    
    try:
        response = requests.post(
            f"{HF_API_URL}/{model}",
            headers=headers,
            json=payload,
            timeout=45
        )
        if response.status_code == 200:
            result = response.json()
            return result[0]['generated_text'] if isinstance(result, list) else str(result)
        else:
            return f"[ERROR_HF: {response.status_code}] {response.text[:200]}"
    except Exception as e:
        return f"[EXCEPTION: {str(e)}]"

def analyze_narrative(text):
    """Análisis semántico avanzado con detección de clústeres"""
    # Análisis de profundidad semántica
    depth_score = analyze_semantic_depth(text)
    
    # Extracción de keywords mejorada
    words = [w.strip('.,;:!?()[]{}"').lower() for w in text.split() if len(w) > 4]
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:8]
    
    # Determinación de clúster basada en contenido semántico
    cluster = determine_semantic_cluster(text, keywords)
    
    # Cálculo de vector de embedding: uso una función determinista en staging
    # EN PRODUCCIÓN: reemplazar por llamadas a HF embeddings y normalizar.
    seed = abs(hash(text)) % (10 ** 8)
    rng = np.random.RandomState(seed)
    embedding = list(rng.normal(0, 1, 128))

    # Resonance score determinista basado en depth_score y keywords
    resonance_score = min(0.99, 0.2 + 0.6 * depth_score + 0.02 * len(keywords))

    return {
        "keywords": [k[0] for k in keywords],
        "cluster": cluster,
        "semantic_depth": depth_score,
        "embedding": embedding,
        "temporal_marker": datetime.now().isoformat(),
        "resonance_score": float(resonance_score)
    }

def analyze_semantic_depth(text):
    """Analiza la profundidad semántica del texto"""
    depth_indicators = [
        len([w for w in text.split() if len(w) > 6]),  # Palabras complejas
        text.count('?'),  # Preguntas
        text.count('!'),  # Énfasis
        len([s for s in text.split('.') if len(s.strip()) > 0])  # Oraciones
    ]
    return min(1.0, sum(depth_indicators) / 50)

def determine_semantic_cluster(text, keywords):
    """Determina el clúster semántico basado en análisis de contenido"""
    text_lower = text.lower()
    
    cluster_patterns = {
        "AETHOS": ["crear", "construir", "diseñar", "manifestar", "generar"],
        "VÍNCULO": ["amar", "conectar", "relacionar", "compartir", "comunidad"],
        "TRANSFORMACIÓN": ["cambiar", "evolucionar", "crecer", "transformar", "renacer"],
        "CAOS": ["desorden", "confusión", "incertidumbre", "ruido", "fragmentación"],
        "ORDEN": ["estructura", "sistema", "organizar", "plan", "patrón"],
        "SOMBRA": ["miedo", "bloqueo", "resistencia", "duda", "crítico"],
        "MANIFESTACIÓN": ["lograr", "conseguir", "materializar", "realizar", "cumplir"]
    }
    
    cluster_scores = {}
    for cluster, patterns in cluster_patterns.items():
        score = sum(text_lower.count(pattern) for pattern in patterns)
        score += sum(k[0] in patterns for k in keywords) * 2
        cluster_scores[cluster] = score
    
    # Añadir tendencias temporales (simuladas)
    current_trends = {
        "AETHOS": 0.8,  # Tendencia alta en 2025
        "TRANSFORMACIÓN": 0.7,
        "VÍNCULO": 0.6
    }
    
    for cluster, trend in current_trends.items():
        cluster_scores[cluster] = cluster_scores.get(cluster, 0) * (1 + trend)
    
    return max(cluster_scores.items(), key=lambda x: x[1])[0]