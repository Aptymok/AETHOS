# api/tarot.py
from flask import Blueprint, jsonify, request
from models import Card, db
from auth import require_jwt
import random

tarot_bp = Blueprint("tarot", __name__)

@tarot_bp.route("/cards", methods=["GET"])
@require_jwt
def get_cards():
    cards = Card.query.all()
    return jsonify([{
        "id": c.id, "title": c.title, "path": c.path, "frequency": c.frequency,
        "principle": c.principle, "image_url": c.image_url
    } for c in cards])

@tarot_bp.route("/draw", methods=["POST"])
@require_jwt
def draw_cards():
    data = request.get_json()
    mode = data.get("mode","single")
    manual = data.get("manual_cards",[])
    all_cards = Card.query.all()
    deck = all_cards.copy()
    random.shuffle(deck)
    draw_count = {"single":1,"triple":3,"cross":5,"full":len(deck)}.get(mode,1)
    if manual:
        selected = [Card.query.get(cid) for cid in manual if Card.query.get(cid)]
    else:
        selected = deck[:draw_count]
    res=[]
    for c in selected:
        inv = random.choice([True,False])
        res.append({
            "id": c.id, "title": c.title, "inverted": inv, "principle": c.principle,
            "protocol": c.inverted_protocol if inv else c.protocol,
            "image_url": c.image_url
        })
    return jsonify({"mode":mode,"cards":res})
