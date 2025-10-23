# api/missions.py
class CollectiveMission(db.Model):
    __tablename__ = "collective_missions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    target_cluster = db.Column(db.String(80))
    required_alignments = db.Column(db.JSON)  # [{cluster: "Aethos", min_alignment: 0.7}]
    current_progress = db.Column(db.Float)
    rewards = db.Column(db.JSON)  # CSS themes, nuevas máscaras, protocolos desbloqueados