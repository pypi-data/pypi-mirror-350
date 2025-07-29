from flask import Blueprint, request, current_app, jsonify, Response
from .. import db
from ..models import Strategy
from ..models import User, Arena
from ..models import Game as GameModel, Result
from ..models import MLModel
from ..arena import Game
from sqlalchemy import select, func, desc, case
from sqlalchemy.orm import aliased
import uuid
import os
from ..safety import safe_import_strategy
from datetime import datetime, timedelta
import logging
from ..validation import validate_strategy_script, StrategyValidationError
from typing import Any, Dict, List, Tuple, Optional
from ..utils import onboarding_required
import tempfile
from azure.storage.blob import BlobServiceClient
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp: Blueprint = Blueprint("strategy", __name__)


@bp.post("/")
@onboarding_required
def create_strategy(user: User):

    now = datetime.utcnow()
    start_of_day = datetime(now.year, now.month, now.day)
    end_of_day = start_of_day + timedelta(days=1)
    already = db.session.execute(
        select(Strategy.id)
        .where(
            Strategy.user_id == user.id,
            Strategy.is_deleted == False,
            Strategy.created_at >= start_of_day,
            Strategy.created_at < end_of_day,
        )
        .limit(1)
    ).scalar_one_or_none()
    # if already is not None:
    # return {"error": "Ma már töltöttél fel stratégiát"}, 400

    data = request.form
    script = data["code"]
    cfg = current_app.config
    src = cfg["STRATEGY_SOURCE"]
    folder = cfg.get("STRATEGY_FOLDER")  # None in blob mode

    # — Step 1: write script to temp file —
    if src == "local":
        os.makedirs(folder, exist_ok=True)
        temp_path = os.path.join(folder, f"{uuid.uuid4()}.py")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(script)
    else:
        tmp = tempfile.NamedTemporaryFile(
            suffix=".py", delete=False, mode="w", encoding="utf-8"
        )
        tmp.write(script)
        tmp.flush()
        temp_path = tmp.name
        tmp.close()

    # — Step 1b: save uploaded model file to temp, if any —
    model_file = request.files.get("model")
    model_temp: Optional[str] = None
    if model_file:
        ext = os.path.splitext(model_file.filename)[1].lower()
        if ext not in {".ts", ".onnx"}:
            return {
                "error": f"Unsupported model type '{ext}'. Allowed: .ts, .onnx"
            }, 400
        tmp_model = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
        model_temp = tmp_model.name
        tmp_model.close()
        model_file.save(model_temp)

    # — Step 2: validate both code & model together —
    try:
        StratCls, elapsed_time = validate_strategy_script(
            script_path=temp_path,
            model_path=model_temp,
        )
    except StrategyValidationError as e:
        os.remove(temp_path)
        if model_temp and os.path.exists(model_temp):
            os.remove(model_temp)
        return {"error": str(e), "solutions": e.suggestions}, 400

    # GDPR‐safe author: drop anything after “@” if username is an email
    raw_username = user.username or ""
    if "@" in raw_username:
        author_part = raw_username.split("@", 1)[0]
    else:
        author_part = raw_username
    author = author_part.replace(" ", "_").replace(".", "")

    # — Step 3: finalize script filename & move/upload —
    # Instantiate once with model_temp (may be None) to read .name safely
    try:
        strat_for_name = StratCls(model_temp)
    except TypeError:
        strat_for_name = StratCls()
    base_name = strat_for_name.name.replace(" ", "_")
    date_tag = datetime.utcnow().strftime("%Y%m%d")
    final_py = f"{base_name}_{author}_{date_tag}.py"
    module_name = final_py[:-3]

    if src == "local":
        final_path = os.path.join(folder, final_py)
        os.rename(temp_path, final_path)
    else:
        blob_cli = BlobServiceClient.from_connection_string(cfg["BLOB_CONN_STRING"])
        container = blob_cli.get_container_client(cfg["BLOB_CONTAINER"])
        blob_path = cfg.get("BLOB_PREFIX", "").rstrip("/") + "/" + final_py
        with open(temp_path, "rb") as fp:
            container.upload_blob(name=blob_path, data=fp, overwrite=True)
        os.remove(temp_path)

    # — Step 4: insert Strategy row —
    strat = Strategy(
        name=strat_for_name.name,
        module_name=module_name,
        user_id=user.id,
        test_runtime=elapsed_time,
    )
    db.session.add(strat)
    db.session.commit()

    # — Step 5: persist the model for real —
    if model_temp:
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        ext = os.path.splitext(model_temp)[1]
        final_model_name = f"{module_name}_{ts}{ext}"

        if cfg["MODEL_SOURCE"] == "local":
            mf_folder = cfg["MODEL_FOLDER"]
            os.makedirs(mf_folder, exist_ok=True)
            final_model_path = os.path.join(mf_folder, final_model_name)
            os.rename(model_temp, final_model_path)
            storage = "local"
            store_path = final_model_path
        else:
            blob_cli = BlobServiceClient.from_connection_string(cfg["BLOB_CONN_STRING"])
            container = blob_cli.get_container_client(cfg["BLOB_CONTAINER"])
            blob_path = cfg["MODEL_BLOB_PREFIX"].rstrip("/") + "/" + final_model_name
            with open(model_temp, "rb") as f:
                container.upload_blob(name=blob_path, data=f, overwrite=True)
            os.remove(model_temp)
            storage = "blob"
            store_path = blob_path

        # upsert MLModel (one-to-one)
        existing = (
            db.session.query(MLModel).filter_by(strategy_id=strat.id).one_or_none()
        )
        if existing:
            existing.filename = final_model_name
            existing.storage = storage
            existing.path = store_path
        else:
            ml = MLModel(
                strategy_id=strat.id,
                filename=final_model_name,
                storage=storage,
                path=store_path,
            )
            db.session.add(ml)

        db.session.commit()

    return {
        "message": "Strategy and model uploaded successfully",
        "module_name": module_name,
        "model_provided": bool(model_temp),
    }, 200


@bp.get("/others")
@onboarding_required
def get_other_strategies():
    # 1) Identify the current user
    user_header = json.loads(request.headers.get("X-User"))
    me = db.session.execute(
        select(User).where(User.oauth_email == user_header["email"])
    ).scalar()
    if not me:
        return {"error": "User not found"}, 404

    # 2) Fetch the last successful regular arena
    last_arena = db.session.execute(
        select(Arena)
        .where(Arena.is_regular == 1, Arena.games_played > 0)
        .order_by(Arena.created_at.desc())
        .limit(1)
    ).scalar()
    if not last_arena:
        return {"error": "No successful regular arena found"}, 404

    # 3) Subquery: avg points per strategy in that arena
    avg_subq = (
        select(
            Result.strategy_id.label("sid"), func.avg(Result.score).label("avg_point")
        )
        .join(GameModel, Result.game_id == GameModel.id)
        .where(GameModel.arena_id == last_arena.id)
        .group_by(Result.strategy_id)
        .subquery()
    )

    # 4) Main query: only “other” strategies, with author and avg
    q = (
        select(
            Strategy.id.label("strategy_id"),
            Strategy.name.label("strategy_name"),
            User.username.label("author"),
            func.coalesce(avg_subq.c.avg_point, 0).label("avg_point_per_game"),
        )
        .select_from(Strategy)
        .join(avg_subq, Strategy.id == avg_subq.c.sid)
        .join(User, Strategy.user_id == User.id)
        .where(Strategy.is_deleted == 0, Strategy.user_id != me.id)
        .order_by(avg_subq.c.avg_point.desc())
    )

    rows = db.session.execute(q).all()

    # 5) Serialize
    others = [
        {
            "id": r.strategy_id,
            "strategy_name": r.strategy_name,
            "author": r.author,
            "avg_point_per_game": float(r.avg_point_per_game),
        }
        for r in rows
    ]

    return jsonify(
        {
            "arena_id": last_arena.id,
            "created_at": last_arena.created_at.isoformat(),
            "strategies": others,
        }
    )


@bp.get("/")
@onboarding_required
def get_strategies() -> List[Dict[str, Any]]:

    user_header = json.loads(request.headers.get("X-User"))

    user = db.session.execute(
        select(User).where(User.oauth_email == user_header["email"])
    ).scalar()

    strategies: List[Strategy] = (
        db.session.execute(
            select(Strategy).where(
                Strategy.is_deleted == False, Strategy.user_id == user.id
            )
        )
        .scalars()
        .all()
    )
    return [
        {"id": strategy.id, "name": strategy.name, "author": strategy.user.name}
        for strategy in strategies
    ]


@bp.get("/<strategy_id>")
@onboarding_required
def get_strategy(strategy_id: int) -> Tuple[Dict[str, Any], int]:
    strategy: Optional[Strategy] = db.session.execute(
        select(Strategy).where(Strategy.id == strategy_id, Strategy.is_deleted == False)
    ).scalar()

    if not strategy:
        return {"error": "Not found"}, 404

    return {"name": strategy.name, "author": strategy.user.name}, 200


@bp.delete("/<strategy_id>")
@onboarding_required
def delete_strategy(strategy_id: int) -> Tuple[Dict[str, Any], int]:
    # @TODO: Implement auth
    return {"error": "Unauthorized"}, 401

    strategy: Optional[Strategy] = db.session.execute(
        select(Strategy).where(Strategy.id == strategy_id, Strategy.is_deleted == False)
    ).scalar()

    if not strategy:
        return {"error": "Not found"}, 404

    strategy.is_deleted = True

    strategy_file: str = os.path.join(
        current_app.config.get("STRATEGY_FOLDER", "instance/strategies"),
        f"{strategy.module_name}.py",
    )

    if os.path.exists(strategy_file):
        new_name: str = os.path.join(
            current_app.config.get("STRATEGY_FOLDER", "instance/strategies"),
            f"DELETED_{strategy.module_name}.del",
        )
        os.rename(strategy_file, new_name)

    db.session.commit()

    return {"message": "OK"}, 200


@bp.post("/compare")
@onboarding_required
def compare_strategies() -> Tuple[Dict[str, Any], int]:
    data: Dict[str, Any] = request.json

    strategy1_id: int = int(data.get("strategy1"))
    strategy2_id: int = int(data.get("strategy2"))
    rounds: int = int(data.get("rounds"))

    strategy1: Optional[Strategy] = db.session.execute(
        select(Strategy).where(
            Strategy.id == strategy1_id, Strategy.is_deleted == False
        )
    ).scalar()
    strategy2: Optional[Strategy] = db.session.execute(
        select(Strategy).where(
            Strategy.id == strategy2_id, Strategy.is_deleted == False
        )
    ).scalar()

    if not strategy1 or not strategy2:
        return {"error": "Strategy not found"}, 404

    try:
        strategy1_class = safe_import_strategy(strategy1.module_name)
    except Exception:
        return {"error": "Strategy 1 load failed"}, 500

    try:
        strategy2_class = safe_import_strategy(strategy2.module_name)
    except Exception:
        return {"error": "Strategy 2 load failed"}, 500

    game: Game = Game(strategy1_class(), strategy2_class())
    game.play_rounds(rounds)

    return {
        "strategy1": game.win1,
        "strategy2": game.win2,
        "ties": game.tie,
    }, 200


@bp.get("/<int:strategy_id>/history")
@onboarding_required
def get_strategy_history(strategy_id: int) -> Response:
    # 1. History per arena: total & average points
    history_q = (
        select(
            GameModel.arena_id.label("arena_id"),
            func.sum(Result.score).label("cumulated_points"),
            func.avg(Result.score).label("avg_score"),
        )
        .join(Result, Result.game_id == GameModel.id)
        .where(
            Result.strategy_id == strategy_id,
            GameModel.is_deleted == False,
            Result.is_deleted == False,
        )
        .group_by(GameModel.arena_id)
        .order_by(GameModel.arena_id)
    )
    arena_stats = db.session.execute(history_q).all()

    history_data = []
    total_points = 0.0
    # We’ll accumulate wins and matches below
    total_matches = 0
    total_wins = 0

    for row in arena_stats:
        history_data.append(
            {
                "arena_id": row.arena_id,
                "cumulated_points": float(row.cumulated_points),
                "avg_score": float(row.avg_score),
            }
        )
        total_points += float(row.cumulated_points)

    # 2. Total matches played by this strategy
    total_matches = (
        db.session.query(func.count(Result.id))
        .filter(
            Result.strategy_id == strategy_id,
            Result.is_deleted == False,
        )
        .scalar()
        or 0
    )

    # 3. Total wins: compare this strategy’s score vs opponent’s score
    other = aliased(Result)
    wins_q = (
        select(func.count())
        .select_from(Result)
        .join(
            other,
            (other.game_id == Result.game_id)
            & (other.strategy_id != Result.strategy_id),
        )
        .where(
            Result.strategy_id == strategy_id,
            Result.score > other.score,
            Result.is_deleted == False,
            other.is_deleted == False,
        )
    )
    total_wins = db.session.execute(wins_q).scalar() or 0

    # 4. Overall averages
    avg_point = (total_points / total_matches) if total_matches else 0
    avg_win_ratio = (total_wins / total_matches) if total_matches else 0

    # 5. Best and worst opponents by average score
    opp_stats_q = (
        select(
            Result.opponent_strategy_id.label("opponent_id"),
            Strategy.name.label("opponent_name"),
            func.avg(Result.score).label("avg_score"),
        )
        .join(Strategy, Strategy.id == Result.opponent_strategy_id)
        .where(
            Result.strategy_id == strategy_id,
            Result.is_deleted == False,
        )
        .group_by(Result.opponent_strategy_id, Strategy.name)
    )

    best = db.session.execute(opp_stats_q.order_by(desc("avg_score")).limit(1)).first()
    worst = db.session.execute(opp_stats_q.order_by("avg_score").limit(1)).first()

    response = {
        "strategy_id": strategy_id,
        "avg_point": avg_point,
        "avg_win_ratio": avg_win_ratio,
        "history": history_data,
        "best_opponent": {
            "opponent_id": best.opponent_id if best else None,
            "opponent_name": best.opponent_name if best else None,
            "avg_score_against": float(best.avg_score) if best else None,
        },
        "worst_opponent": {
            "opponent_id": worst.opponent_id if worst else None,
            "opponent_name": worst.opponent_name if worst else None,
            "avg_score_against": float(worst.avg_score) if worst else None,
        },
    }

    return jsonify(response)


@bp.get("/last_created")
@onboarding_required
def get_last_created_strategy(user: User):
    """
    Return the creation time of the most recently created strategy
    belonging to the current user.
    """
    # find the latest non‐deleted strategy
    last_created: Optional[datetime] = db.session.execute(
        select(Strategy.created_at)
        .where(Strategy.user_id == user.id, Strategy.is_deleted == False)
        .order_by(Strategy.created_at.desc())
        .limit(1)
    ).scalar_one_or_none()

    if last_created is None:
        return {"error": "No strategies found"}, 404

    return jsonify({"created_at": last_created.isoformat()}), 200
