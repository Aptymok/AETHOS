# api/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(32), default="testigo")
    coherence = db.Column(db.Float, default=0.5)  # 0..1
    style = db.Column(db.Text, nullable=True)     # CSS personalizado (string)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    path = db.Column(db.String(80))
    frequency = db.Column(db.String(80))
    principle = db.Column(db.String(200))
    protocol = db.Column(db.Text)
    inverted_protocol = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    # Additional fields
    resonance_type = db.Column(db.String(50))  # 'temporal', 'espacial', 'relacional'
    activation_cost = db.Column(db.Float)      # 'energía' simbólica para activar
    dependencies = db.Column(db.JSON)          # IDs de cartas requeridas
    evolution_path = db.Column(db.JSON)        # Cartas a las que puede evolucionar

class Manifest(db.Model):
    __tablename__ = "manifests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    intention = db.Column(db.Text)
    mask = db.Column(db.String(80))
    entropy = db.Column(db.Float)
    alignment = db.Column(db.Float)
    keywords = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Diagnostic(db.Model):
    __tablename__ = "diagnostics"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    query = db.Column(db.JSON)
    result = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
