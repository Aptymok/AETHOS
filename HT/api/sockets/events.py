def register_socket_events(socketio):
    
    @socketio.on('connect')
    def handle_connect():
        request = get_flask_request()
        print(f"Client connected: {request.sid}")
        get_emit()()('connection_established', {
            'status': 'connected',
            'timestamp': datetime.now().isoformat(),
            'system': 'AETHOS_ACTIVE'
        })
    
    @socketio.on('join_resonance_cluster')
    def handle_join_cluster(data):
        cluster = data.get('cluster', 'global')
        user_id = data.get('user_id')
        
        get_join_room()()(cluster)
        get_emit()()('cluster_joined', {
            'cluster': cluster,
            'user_count': get_cluster_user_count(cluster),
            'resonance_level': get_cluster_resonance(cluster)
        }, room=cluster)
        
        print(f"User {user_id} joined cluster {cluster}")
    
    @socketio.on('manifestation_event')
    def handle_manifestation(data):
        cluster = data.get('cluster')
        manifestation_data = data.get('manifestation', {})
        
        # Emitir a todos en el clÃºster
        get_emit()()('resonance_update', {
            'type': 'manifestation',
            'data': manifestation_data,
            'timestamp': datetime.now().isoformat(),
            'collective_impact': calculate_collective_impact(cluster)
        }, room=cluster)
    
    @socketio.on('request_collective_insight')
    def handle_collective_insight(data):
        user_id = data.get('user_id')
        cluster = data.get('cluster')
        intention = data.get('intention')
        
        # Generar insight colectivo basado en manifestaciones del clÃºster
        collective_insight = generate_collective_insight(cluster, intention)
        
        get_emit()()('collective_insight', {
            'insight': collective_insight,
            'based_on_manifestations': get_recent_cluster_manifestations(cluster, 5),
            'resonance_factor': calculate_resonance_factor(intention, cluster)
        })
    
    @socketio.on('disconnect')
    def handle_disconnect():
        request = get_flask_request()
        print(f"Client disconnected: {request.sid}")
def emit_resonance_update(cluster, data):
    """Función helper para emitir actualizaciones de resonancia"""
    try:
        # Esta es una implementación básica
        print(f"[RESONANCE] Cluster: {cluster}, Data: {data}")
    except Exception as e:
        print(f"Error emitting resonance update: {e}")
