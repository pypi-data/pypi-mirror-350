# File: rpsa_backend/public_api/routes/strategies.py

"""
/strategies – Public endpoints for retrieving aggregate and head-to-head
performance metrics for strategies, scoped to arenas visible to the caller.

Endpoints:
  • GET /strategies/regular
      Paginated list of strategies with average points per game & other
      metrics, calculated only over *regular* arenas (public).
  • GET /strategies/irregular
      Same, but only over *irregular* arenas started by you (private).
  • GET /strategies/<strategy_id>/results
      Legacy single-strategy summary, now includes avg points/game.
  • GET /strategies/<strategy_id>/head_to_head
      Per-opponent aggregates including avg points/game.
"""

from flask import Blueprint, jsonify, request, g, abort
from sqlalchemy import func, or_
from ..auth import api_key_required
from ..schemas import StrategySummarySchema, MatchupSchema
from ..utils import get_accessible_arena_or_404
from ...public_api.extensions import limiter, cache
from ...models import (
    Strategy as StrategyModel,
    Result as ResultModel,
    Game as GameModel,
    Arena as ArenaModel,
)
from ... import db

bp = Blueprint("strategies", __name__, url_prefix="/strategies")


def _arena_ids_subquery(user, regular: bool):
    """
    Return a subquery of arena IDs, filtering by regular vs. irregular + ownership.
    """
    q = db.session.query(ArenaModel.id).filter(
        ArenaModel.is_deleted == False,
        ArenaModel.is_regular == regular,
    )
    if not regular:
        q = q.filter(ArenaModel.user_id == user.id)
    return q.subquery()


def _stats_subquery(arena_ids):
    """
    Build a subquery of aggregated sums and counts per strategy, over the given arenas.
    """
    return (
        db.session.query(
            StrategyModel.id.label("strategy_id"),
            StrategyModel.module_name.label("strategy_name"),
            func.coalesce(func.sum(ResultModel.score), 0.0).label("sum_score"),
            func.count(ResultModel.id).label("games_count"),
            func.coalesce(func.sum(ResultModel.wins), 0).label("wins"),
            func.coalesce(func.sum(ResultModel.losses), 0).label("losses"),
            func.coalesce(func.sum(ResultModel.ties), 0).label("ties"),
            func.coalesce(func.sum(ResultModel.net_score), 0).label("net_score"),
        )
        .join(ResultModel, StrategyModel.id == ResultModel.strategy_id)
        .join(GameModel, ResultModel.game_id == GameModel.id)
        .filter(GameModel.arena_id.in_(arena_ids))
        .group_by(StrategyModel.id, StrategyModel.module_name)
        .subquery()
    )


def _list_strategies_core(regular: bool):
    user = g.current_user
    arena_ids = _arena_ids_subquery(user, regular)
    stats_sq = _stats_subquery(arena_ids)

    # Base query over the stats subquery
    q = db.session.query(stats_sq)

    # Sorting
    sort = request.args.get("sort", "avg_ppg,desc")
    field, _, direction = sort.partition(",")
    direction = direction or "desc"

    if field in {"avg_ppg", "wins", "losses", "ties", "net_score"} and direction in {
        "asc",
        "desc",
    }:
        if field == "avg_ppg":
            col = stats_sq.c.sum_score / stats_sq.c.games_count
        else:
            col = getattr(stats_sq.c, field)
        q = q.order_by(col.desc() if direction == "desc" else col)

    # Pagination parameters
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", 20)), 1), 100)
    except ValueError:
        page, per_page = 1, 20

    # Total count
    total = db.session.query(func.count()).select_from(stats_sq).scalar() or 0
    pages = (total + per_page - 1) // per_page if total else 1

    # Fetch this page
    items = q.limit(per_page).offset((page - 1) * per_page).all()

    # Build payload
    payload = []
    for r in items:
        avg_ppg = float(r.sum_score) / r.games_count if r.games_count else 0.0
        plays = r.wins + r.losses + r.ties
        win_rate = (r.wins / (r.wins + r.losses)) if (r.wins + r.losses) else 0.0

        payload.append(
            {
                "strategy_id": r.strategy_id,
                "strategy_name": r.strategy_name,
                "plays": plays,
                "wins": int(r.wins),
                "losses": int(r.losses),
                "ties": int(r.ties),
                "avg_points_per_game": round(avg_ppg, 4),
                "games_played": plays,
                "total_score": float(r.sum_score),
                "net_score": int(r.net_score),
                "win_rate": round(win_rate, 4),
            }
        )

    return jsonify(
        {
            "data": StrategySummarySchema(many=True).dump(payload),
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": pages,
            },
        }
    )


@bp.get("/regular")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60, query_string=True)
def list_regular_strategies():
    """
    GET /strategies/regular
    Paginated list of strategies with average points/game & other stats,
    computed over *regular* (public) arenas only.
    """
    return _list_strategies_core(regular=True)


@bp.get("/irregular")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60, query_string=True)
def list_irregular_strategies():
    """
    GET /strategies/irregular
    Paginated list of strategies with average points/game & other stats,
    computed over *irregular* arenas you started.
    """
    return _list_strategies_core(regular=False)


@bp.get("/<int:strategy_id>/results")
@api_key_required
@limiter.limit("200 per hour")
@cache.cached(timeout=60)
def get_strategy_results(strategy_id):
    """
    GET /strategies/<strategy_id>/results
    Legacy single-strategy summary. Returns the same fields as
    list_{regular,irregular}, but for one strategy across all accessible arenas.
    """
    # Validate existence
    strat = db.session.get(StrategyModel, strategy_id)
    if not strat:
        abort(404, description="Strategy not found.")

    # Build arena filter (regular OR owned)
    arena_ids = (
        db.session.query(ArenaModel.id)
        .filter(
            ArenaModel.is_deleted == False,
            or_(ArenaModel.is_regular == True, ArenaModel.user_id == g.current_user.id),
        )
        .subquery()
    )

    stats_sq = _stats_subquery(arena_ids)
    row = (
        db.session.query(stats_sq)
        .filter(stats_sq.c.strategy_id == strategy_id)
        .one_or_none()
    )

    if not row:
        payload = {
            "strategy_id": strategy_id,
            "strategy_name": strat.module_name,
            "plays": 0,
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "avg_points_per_game": 0.0,
            "games_played": 0,
            "total_score": 0.0,
            "net_score": 0,
            "win_rate": 0.0,
        }
    else:
        avg_ppg = float(row.sum_score) / row.games_count if row.games_count else 0.0
        plays = row.wins + row.losses + row.ties
        win_rate = (
            (row.wins / (row.wins + row.losses)) if (row.wins + row.losses) else 0.0
        )

        payload = {
            "strategy_id": row.strategy_id,
            "strategy_name": row.strategy_name,
            "plays": plays,
            "wins": int(row.wins),
            "losses": int(row.losses),
            "ties": int(row.ties),
            "avg_points_per_game": round(avg_ppg, 4),
            "games_played": plays,
            "total_score": float(row.sum_score),
            "net_score": int(row.net_score),
            "win_rate": round(win_rate, 4),
        }

    return jsonify(StrategySummarySchema().dump(payload))


@bp.get("/<int:strategy_id>/head_to_head")
@api_key_required
@limiter.limit("100 per hour")
@cache.cached(timeout=60)
def strategy_head_to_head(strategy_id):
    """
    GET /strategies/<strategy_id>/head_to_head
    For the given strategy, returns per-opponent aggregates across
    all accessible arenas, including avg points/game.
    """
    # Validate existence
    strat = db.session.get(StrategyModel, strategy_id)
    if not strat:
        abort(404, description="Strategy not found.")

    # Build arena filter (regular OR owned)
    arena_ids = (
        db.session.query(ArenaModel.id)
        .filter(
            ArenaModel.is_deleted == False,
            or_(ArenaModel.is_regular == True, ArenaModel.user_id == g.current_user.id),
        )
        .subquery()
    )

    rows = (
        db.session.query(
            ResultModel.strategy_id,
            ResultModel.opponent_strategy_id,
            func.coalesce(func.sum(ResultModel.score), 0.0).label("sum_score"),
            func.count(ResultModel.id).label("games_count"),
            func.coalesce(func.sum(ResultModel.wins), 0).label("wins"),
            func.coalesce(func.sum(ResultModel.losses), 0).label("losses"),
            func.coalesce(func.sum(ResultModel.ties), 0).label("ties"),
            func.coalesce(func.sum(ResultModel.net_score), 0).label("net_score"),
        )
        .join(GameModel, ResultModel.game_id == GameModel.id)
        .filter(
            ResultModel.strategy_id == strategy_id,
            GameModel.arena_id.in_(arena_ids),
        )
        .group_by(ResultModel.strategy_id, ResultModel.opponent_strategy_id)
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
                "opponent_strategy_id": r.opponent_strategy_id,
                "wins": int(r.wins),
                "losses": int(r.losses),
                "ties": int(r.ties),
                "avg_points_per_game": round(avg_ppg, 4),
                "net_score": int(r.net_score),
                "win_rate": round(win_rate, 4),
                "games_played": int(r.games_count),
            }
        )

    return jsonify(MatchupSchema(many=True).dump(data))
