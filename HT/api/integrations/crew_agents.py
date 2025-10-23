# api/crew_agents.py
# Simple wrapper to represent masks. In production, each mask uses a model call.
from api.migrations.integrations.huggingface import generate_text

class Agent:
    def __init__(self, name, prompt_template):
        self.name = name
        self.prompt_template = prompt_template
    def respond(self, intention, analysis):
        prompt = self.prompt_template.format(intention=intention, keywords=", ".join(analysis["keywords"]))
        return generate_text(prompt)

def assign_mask(mask_name):
    templates = {
        "Narrador": "Eres NARRADOR. Reescribe con lirismo: {intention}. Contexto: {keywords}.",
        "Arquitecto": "Eres ARQUITECTO. Diseña un plan en pasos concretos para: {intention}. Considera: {keywords}.",
        "Visionario": "Eres VISIONARIO. Expón implicaciones futuras y tendencias para: {intention}. Usa: {keywords}.",
        "Sombra": "Eres SOMBRA. Apunta bloqueos y contradicciones en: {intention}. Palabras: {keywords}.",
        "Oráculo": "Eres ORÁCULO. Conecta la intención con patrones colectivos: {intention}. Claves: {keywords}."
    }
    tpl = templates.get(mask_name, templates["Narrador"])
    return Agent(mask_name, tpl)
