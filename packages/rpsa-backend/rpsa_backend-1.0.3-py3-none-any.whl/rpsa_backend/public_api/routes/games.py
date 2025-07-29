# File: rpsa_backend/public_api/routes/games.py

"""
/games – Public endpoints for browsing and retrieving individual Game results.

• GET /games/regular
    Paginated list of games from all *regular* arenas (public).
• GET /games/irregular
    Paginated list of games from your *irregular* arenas (private to you).
• GET /games/<game_id>
    Full result set (one row per strategy) for a single game,
    provided its parent arena is visible (regular or owned by you).
"""

from flask import Blueprint, jsonify, request, g
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased

from ..auth import api_key_required
from ..schemas import ResultSchema, GameSummarySchema
from ..utils import paginate_query, get_accessible_arena_or_404
from ...public_api.extensions import limiter, cache
from ...models import Arena as ArenaModel, Game as GameModel, Result as ResultModel
from ... import db

bp = Blueprint("games", __name__, url_prefix="/games")


def _base_game_query(user, *, regular: bool):
    """
    Return a Query for GameModel rows whose parent arenas are either
    regular (public) or your own irregular arenas.
    """
    arena_ids = (
        db.session.query(ArenaModel.id)
        .filter(
            ArenaModel.is_deleted == False,
            ArenaModel.is_regular == regular,
            ArenaModel.user_id == (None if regular else user.id),
        )
        .subquery()
    )
    return db.session.query(GameModel).filter(GameModel.arena_id.in_(arena_ids))


@bp.get("/regular")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60, query_string=True)
def list_regular_games():
    """
    GET /games/regular
    Paginated list of all games from *regular* arenas.
    """
    return _list_games_core(regular=True)


@bp.get("/irregular")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60, query_string=True)
def list_irregular_games():
    """
    GET /games/irregular
    Paginated list of all games from your *irregular* arenas.
    """
    return _list_games_core(regular=False)


def _list_games_core(regular: bool):
    """
    Shared implementation for listing games, with pagination, sorting,
    and per-game average‐score injection.
    """
    user = g.current_user
    q = _base_game_query(user, regular=regular)

    # Sorting support
    sort = request.args.get("sort", "game_number,asc")
    field, _, direction = sort.partition(",")
    direction = direction or "asc"
    if field in {"game_number", "runtime"} and direction in {"asc", "desc"}:
        col = getattr(GameModel, field)
        q = q.order_by(col.desc() if direction == "desc" else col)

    # We also want to add each game’s two normalized scores.
    # We'll let the serializer ask for them separately:
    return paginate_query(q, GameSummarySchema)


@bp.get("/<int:game_id>")
@api_key_required
@limiter.limit("200 per hour")
@cache.cached(timeout=60)
def get_game_results(game_id):
    """
    GET /games/<game_id>
    Return all Result rows for a single game—only if its arena is
    regular or owned by you.
    """
    # 1) fetch game & check arena visibility
    game = db.session.query(GameModel).get(game_id)
    if not game:
        return jsonify({"error": "Game not found."}), 404

    # enforce regular vs. irregular access
    get_accessible_arena_or_404(game.arena_id, g.current_user)

    # 2) pull and return results
    results = (
        db.session.query(ResultModel)
        .filter_by(game_id=game_id, is_deleted=False)
        .order_by(ResultModel.strategy_id)
        .all()
    )
    return jsonify(ResultSchema(many=True).dump(results))
