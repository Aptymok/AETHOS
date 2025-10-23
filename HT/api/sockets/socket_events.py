# api/socket_events.py
from flask_socketio import join_room, leave_room, emit
import random
def register_socket_events(socketio):
    @socketio.on("connect")
    def _():
        print("socket connected")

    @socketio.on("join_cluster")
    def _join(data):
        cluster = data.get("cluster","Aethos")
        join_room(cluster)
        emit("joined_cluster", {"cluster":cluster})

    @socketio.on("sync_manifest")
    def _sync(data):
        cluster = data.get("cluster","Aethos")
        payload = {"entropy": random.random(), "alignment": random.random()}
        emit("cluster_update", payload, room=cluster)

def send_cluster_update(cluster, payload):
    # import socketio server instance lazily to avoid cycles
    try:
        from app import socketio
        socketio.emit("cluster_update", payload, room=cluster)
    except Exception as e:
        print("socket emit failed:", e)
