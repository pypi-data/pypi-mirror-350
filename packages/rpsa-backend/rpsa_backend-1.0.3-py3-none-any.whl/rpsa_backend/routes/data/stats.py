from flask import Blueprint, request, jsonify
from rpsa_backend.models import db  # Adjust based on your project structure
from rpsa_backend.models import User, Strategy, Arena, Game

bp = Blueprint("data/stats", __name__)


@bp.route("/get_stats", methods=["GET"])
def get_stats():
    authors_count = db.session.query(User).filter(User.is_deleted == False).count()
    strategies_count = (
        db.session.query(Strategy).filter(Strategy.is_deleted == False).count()
    )
    arenas_count = db.session.query(Arena).filter(Arena.is_deleted == False).count()
    games_count = db.session.query(Game).filter(Game.is_deleted == False).count()

    return jsonify(
        {
            "authors": authors_count,
            "strategies": strategies_count,
            "arenas": arenas_count,
            "games": games_count,
        }
    )
