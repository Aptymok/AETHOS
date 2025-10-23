OPERATIONAL STANDARD OPERATING PROCEDURE (SOP) - AETHOS

Resumen corto:
Este SOP resume los pasos mínimos para operar AETHOS en staging y pasar a producción.

1) Variables de entorno críticas
- HUGGINGFACE_TOKEN
- NEWS_API_KEY
- NOAA_API_KEY (o proveedor de datos geomagnéticos)
- REDIS_URL (opcional)
- DATABASE_URL

2) Preparación de entorno (Windows PowerShell)
# Instalar dependencias (si falta)
# En la carpeta api/migrations
pip install -r requirements.txt

3) Verificaciones rápidas
- Revisar que `REACT_APP_SIMULATE` esté desactivado en producción en `web/`.
- Ejecutar endpoint de health-check (si existe): GET /health
- Ejecutar endpoints básicos: GET /resonance/external y GET /resonance/neural

4) Recomendaciones de despliegue
- Usar Docker Compose en producción con secrets gestionados.
- Rotar claves cada 90 días.

5) Lista de stubs detectados (acción requerida)
- `core/resonance._simulate_geomagnetic_data` -> Reemplazar por adaptador NOAA
- `integrations/huggingface.analyze_narrative` -> Reemplazar embeddings por HF embeddings
- Front-end: toggles para simulado/real

6) Kill-switch operativo
- Implementar endpoint POST /ops/pause-all que pause emisiones en tiempo real (no implementado por defecto).

7) Testing mínimo
- Crear tests de smoke para endpoints de resonancia y tarot.

Notas finales:
- Este SOP es intencionalmente corto. Para una operación completa, crear runbooks por rol (SRE, Integraciones, Ops Lead).