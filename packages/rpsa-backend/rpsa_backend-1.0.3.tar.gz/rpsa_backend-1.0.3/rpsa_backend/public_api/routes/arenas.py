from flask import Blueprint, jsonify, request, g
from sqlalchemy import func, desc
from ..auth import api_key_required
from ..schemas import (
    ArenaSchema,
    GameSummarySchema,
    LeaderboardSchema,
    MatchupSchema,
)
from ..utils import paginate_query, get_accessible_arena_or_404
from ...public_api.extensions import limiter, cache
from ...models import (
    Arena as ArenaModel,
    Game as GameModel,
    Result as ResultModel,
    Strategy as StrategyModel,
)
from ... import db

bp = Blueprint("arenas", __name__, url_prefix="/arenas")


@bp.get("/regular")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60, query_string=True)
def list_regular_arenas():
    """
    GET /arenas/regular
    Paginated list of all **public** (regular) arenas.
    """
    q = (
        db.session.query(ArenaModel)
        .filter(
            ArenaModel.is_deleted == False,
            ArenaModel.is_regular == True,
        )
        .order_by(ArenaModel.created_at.desc())
    )
    return paginate_query(q, ArenaSchema)


@bp.get("/irregular")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60, query_string=True)
def list_irregular_arenas():
    """
    GET /arenas/irregular
    Paginated list of arenas **you** started (irregular arenas).
    """
    user = g.current_user
    q = (
        db.session.query(ArenaModel)
        .filter(
            ArenaModel.is_deleted == False,
            ArenaModel.is_regular == False,
            ArenaModel.user_id == user.id,
        )
        .order_by(ArenaModel.created_at.desc())
    )
    return paginate_query(q, ArenaSchema)


@bp.get("/<int:arena_id>")
@api_key_required
@limiter.limit("200 per hour")
def get_arena(arena_id):
    """
    GET /arenas/<arena_id>
    Retrieve metadata & aggregates for one arena, if it's public or yours.
    """
    arena = get_accessible_arena_or_404(arena_id, g.current_user)
    return jsonify(ArenaSchema().dump(arena))


@bp.get("/<int:arena_id>/games")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60, query_string=True)
def list_arena_games(arena_id):
    """
    GET /arenas/<arena_id>/games
    Paginated list of games in a specific arena (visible to you).
    Query parameters:
      - page, per_page
      - sort=<field>,<asc|desc> (allowed: game_number, runtime, wins_a, wins_b, ties)
    """
    # ensure arena is accessible
    get_accessible_arena_or_404(arena_id, g.current_user)

    base_q = db.session.query(GameModel).filter_by(arena_id=arena_id)

    # Sorting
    sort = request.args.get("sort", "game_number,asc")
    field, _, direction = sort.partition(",")
    direction = direction or "asc"
    sortable = {
        "game_number": GameModel.game_number,
        "runtime": GameModel.runtime,
        "wins_a": GameModel.wins_a,
        "wins_b": GameModel.wins_b,
        "ties": GameModel.ties,
    }
    if field in sortable and direction in {"asc", "desc"}:
        col = sortable[field]
        base_q = base_q.order_by(col.desc() if direction == "desc" else col)

    return paginate_query(base_q, GameSummarySchema)


@bp.get("/<int:arena_id>/leaderboard")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60)
def arena_leaderboard(arena_id):
    """
    GET /arenas/<arena_id>/leaderboard
    Returns per-strategy ranking sorted by average points per game.
    """
    arena = get_accessible_arena_or_404(arena_id, g.current_user)

    # Define the avg‐points‐per‐game expression
    avg_expr = func.sum(ResultModel.score) / func.count(ResultModel.id)

    # Query sums/counts and order by the average (DESC)
    rows = (
        db.session.query(
            ResultModel.strategy_id,
            StrategyModel.module_name.label("strategy_name"),
            func.sum(ResultModel.score).label("sum_score"),
            func.count(ResultModel.id).label("games_count"),
            func.sum(ResultModel.wins).label("wins"),
            func.sum(ResultModel.losses).label("losses"),
            func.sum(ResultModel.ties).label("ties"),
            func.sum(ResultModel.net_score).label("net_score"),
        )
        .join(GameModel, ResultModel.game_id == GameModel.id)
        .join(StrategyModel, StrategyModel.id == ResultModel.strategy_id)
        .filter(GameModel.arena_id == arena.id)
        .group_by(ResultModel.strategy_id, StrategyModel.module_name)
        # apply DESC to the entire avg expression:
        .order_by(desc(avg_expr))
        .all()
    )

    data = []
    for r in rows:
        avg_ppg = float(r.sum_score) / r.games_count if r.games_count else 0.0
        plays = r.wins + r.losses
        win_rate = (r.wins / plays) if plays else 0.0

        data.append(
            {
                "strategy_id": r.strategy_id,
                "strategy_name": r.strategy_name,
                "avg_points_per_game": round(avg_ppg, 4),
                "wins": int(r.wins),
                "losses": int(r.losses),
                "ties": int(r.ties),
                "net_score": int(r.net_score),
                "win_rate": round(win_rate, 4),
                "games_played": int(r.games_count),
            }
        )

    return jsonify(LeaderboardSchema(many=True).dump(data))


@bp.get("/<int:arena_id>/matchups")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60)
def arena_matchups(arena_id):
    """
    GET /arenas/<arena_id>/matchups
    Head-to-head aggregates for each pair, including avg_points_per_game.
    """
    arena = get_accessible_arena_or_404(arena_id, g.current_user)

    rows = (
        db.session.query(
            ResultModel.strategy_id,
            ResultModel.opponent_strategy_id,
            func.sum(ResultModel.wins).label("wins"),
            func.sum(ResultModel.losses).label("losses"),
            func.sum(ResultModel.ties).label("ties"),
            func.sum(ResultModel.net_score).label("net_score"),
            func.sum(ResultModel.score).label("total_score"),
            func.count(ResultModel.id).label("games_count"),
        )
        .join(GameModel, ResultModel.game_id == GameModel.id)
        .filter(GameModel.arena_id == arena.id)
        .group_by(
            ResultModel.strategy_id,
            ResultModel.opponent_strategy_id,
        )
        .all()
    )

    data = []
    for r in rows:
        plays = r.wins + r.losses
        win_rate = (r.wins / plays) if plays else 0.0
        avg_ppg = float(r.total_score) / r.games_count if r.games_count else 0.0
        data.append(
            {
                "strategy_id": r.strategy_id,
                "opponent_strategy_id": r.opponent_strategy_id,
                "wins": int(r.wins),
                "losses": int(r.losses),
                "ties": int(r.ties),
                "net_score": int(r.net_score),
                "win_rate": round(win_rate, 4),
                "avg_points_per_game": round(avg_ppg, 4),
            }
        )

    return jsonify(MatchupSchema(many=True).dump(data))
