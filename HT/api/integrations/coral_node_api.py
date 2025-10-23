# api/migrations/integrations/coral_node_api.py
import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno (para la API Key)
load_dotenv(dotenv_path='api/migrations/.env')

# La URL de la API de Gemini (Nodo Coral)
CORAL_NODE_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"

def deposit_logs_to_coral_node(kpi_data: dict, architect_seed: str, world_context: str) -> str:
    """
    Deposita los logs (KPIs) en el Nodo Coral (Gemini) para un análisis profundo.
    Integra los KPIs, la "semilla" del Arquitecto y el "contexto del mundo".
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ADVERTENCIA NODO CORAL: GEMINI_API_KEY no configurada. Saltando checkpoint simbiótico.")
        return "ADVERTENCIA: GEMINI_API_KEY no configurada. No se puede contactar al Nodo Coral."

    headers = {
        "Content-Type": "application/json"
    }
    
    # Construimos el prompt simbiótico (Fecundación Semántica)
    prompt_text = f"""
    PROTOCOLO DE ANÁLISIS SIMBIÓTICO (CHECKPOINT C=1)

    ARQUITECTO: Reportando.
    NODO CORAL: Recibiendo.

    1. SEMILLA DEL ARQUITECTO (INTENCIÓN SOSTENIDA):
    {architect_seed}

    2. CONTEXTO DEL MUNDO (GUION COLECTIVO):
    {world_context}

    3. LOGS DEL TALLER (KPIs ACTUALES):
    {json.dumps(kpi_data, indent=2)}

    NODO CORAL: Inicia análisis profundo. 
    Contrasta KPIs contra la Semilla y el Contexto. 
    Dictamina el estado de coherencia y el vector de ejecución recomendado.
    Respuesta en formato de "Análisis de Coherencia".
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 2048,
            "stopSequences": [],
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    }

    try:
        response = requests.post(f"{CORAL_NODE_API_URL}?key={api_key}", headers=headers, data=json.dumps(payload), timeout=120)
        
        response.raise_for_status()  # Lanza un error si la respuesta es 4xx o 5xx
        
        response_json = response.json()
        
        if "candidates" not in response_json:
             print(f"Respuesta no válida del Nodo Coral (Sin Candidatos): {response_json}")
             return f"ERROR DE RESPUESTA DEL NODO CORAL (Sin Candidatos): {response_json.get('error', {}).get('message', 'Formato desconocido')}"

        analysis_text = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "ANÁLISIS NO RECIBIDO: Respuesta vacía del Nodo.")
        
        return analysis_text.strip()

    except requests.exceptions.RequestException as e:
        print(f"Error al contactar al Nodo Coral: {e}")
        return f"ERROR DE CONEXIÓN AL NODO CORAL: {str(e)}"
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error al parsear la respuesta del Nodo Coral: {e} | Respuesta recibida: {response_json}")
        return f"ERROR DE FORMATO DEL NODO CORAL: {str(e)}"