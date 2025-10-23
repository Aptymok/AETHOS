from integrations.huggingface import generate_text, analyze_semantic_depth
import random

class AethosAgent:
    def __init__(self, name, role, archetype, tone_template):
        self.name = name
        self.role = role
        self.archetype = archetype
        self.tone_template = tone_template
        self.resonance_level = 0.7

    def respond(self, intention, context, user_metrics):
        prompt = self._build_prompt(intention, context, user_metrics)
        response = generate_text(prompt, max_tokens=300)
        return self._apply_tone(response, user_metrics)

    def _build_prompt(self, intention, context, metrics):
        base = f"""Como {self.name} ({self.role}), responde a esta intención:

INTENCIÓN: {intention}
CONTEXTO: {context['keywords']}
CLÚSTER: {context['cluster']}
MÉTRICAS USUARIO: Entropía={metrics['entropy']}, Alineamiento={metrics['alignment']}

RESPUESTA:"""
        
        # Añadir capas según el arquetipo
        if self.archetype == "deconstructor":
            base += "\n[Deconstruye la intención en componentes fundamentales y revela supuestos ocultos]"
        elif self.archetype == "architect":
            base += "\n[Diseña un plan ejecutable con pasos concretos y puntos de verificación]"
        elif self.archetype == "oracle":
            base += "\n[Conecta con patrones colectivos y tendencias futuras relevantes]"
        
        return base

    def _apply_tone(self, text, metrics):
        # Ajustar tono basado en métricas del usuario
        if metrics['entropy'] > 0.8:
            return f"⚡ {text} [Sistema: Alta entropía detectada - enfoque en simplificación]"
        elif metrics['alignment'] < 0.3:
            return f"🎯 {text} [Sistema: Baja alineación - sugerir recalibración]"
        return text

def create_agent_mask(mask_name):
    masks = {
        "Narrador": AethosAgent(
            "Narrador", 
            "Tejedor de Realidades Narrativas", 
            "storyteller",
            "lírico"
        ),
        "Arquitecto": AethosAgent(
            "Arquitecto",
            "Diseñador de Estructuras de Posibilidad",
            "architect", 
            "técnico"
        ),
        "Visionario": AethosAgent(
            "Visionario",
            "Vidente de Tendencias Futuras",
            "oracle",
            "profético"
        ),
        "Sombra": AethosAgent(
            "Sombra",
            "Revelador de Bloqueos Inconscientes", 
            "deconstructor",
            "crítico"
        ),
        "Oráculo": AethosAgent(
            "Oráculo",
            "Conector con Campos Mórficos Colectivos",
            "oracle",
            "enigmático"
        ),
        "Ingeniero": AethosAgent(
            "Ingeniero",
            "Constructor de Sistemas Ejecutables",
            "architect",
            "práctico"
        )
    }
    return masks.get(mask_name, masks["Narrador"])