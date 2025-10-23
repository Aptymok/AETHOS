# Importación diferida para evitar circular imports
def register_socket_events(socketio):
    from .events import register_socket_events as _register_socket_events
    return _register_socket_events(socketio)

def emit_resonance_update(cluster, data):
    from .events import emit_resonance_update as _emit_resonance_update
    return _emit_resonance_update(cluster, data)