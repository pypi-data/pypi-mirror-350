import logging.config
from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select, func, desc, union_all, and_, case
from sqlalchemy.orm import aliased
from .. import db, executor
from ..models import (
    Strategy as StrategyModel,
    Arena as ArenaModel,
    Game as GameModel,
    User as UserModel,
    Result as ResultModel,
    MLModel as MLModel,
)
from ..arena import Arena
from typing import List, Dict, TypedDict
from ..safety import safe_import_strategy
import logging
import time
from ..utils import onboarding_required
import json

bp = Blueprint("arena", __name__)


def run_arena_and_update_runtime(arena: Arena, arena_id: int):
    """
    Runs the arena and updates the database record with the total runtime.
    """
    start_time = time.perf_counter()
    try:
        # Run the arena - note: arena.start() should be a blocking call
        arena.start()
    except Exception as e:
        logging.exception("Error while running the arena: %s", e)
    finally:
        runtime = time.perf_counter() - start_time
        # Update the arena record in the database with the runtime.
        # Make sure you're in the appropriate app context if needed.
        with db.session.begin():
            arena_doc = db.session.get(ArenaModel, arena_id)

            arena_doc.runtime = runtime
            db.session.commit()
        logging.info(f"Arena {arena_id} finished running in {runtime:.2f} seconds.")

    return 0


@bp.post("/")
@onboarding_required
def create_arena():

    user_header = json.loads(request.headers.get("X-User"))

    user = db.session.execute(
        select(UserModel).where(UserModel.oauth_email == user_header["email"])
    ).scalar()

    data: dict = request.json
    strategies = data.get("strategies", [])
    rounds_per_game = int(data.get("rounds_per_game"))
    games_per_pair = int(data.get("games_per_pair"))
    max_points = int(data.get("max_points"))
    is_competition = int(data.get("participateInCompetition"))
    user_id = user.id
    logging.info("Received data: %s", data)

    # Import the strategy classes.
    strategy_classes = []
    for strategy_id in strategies:
        logging.info(f"Processing strategy_id: {strategy_id}")
        strategy = db.session.execute(
            select(StrategyModel).where(
                StrategyModel.id == strategy_id, StrategyModel.is_deleted == False
            )
        ).scalar()
        if strategy:
            try:
                strategy_class = safe_import_strategy(strategy.module_name)
                strategy_classes.append(strategy_class)
            except Exception as e:
                return {"error": str(e)}, 400

    logging.info(f"Strategy classes imported: {strategy_classes}")

    # Create and commit the arena document.
    arena_doc = ArenaModel(
        user_id=user_id,
        number_strategies=len(strategies),
        rounds_per_game=rounds_per_game,
        games_per_pair=games_per_pair,
        max_points=max_points,
        is_regular=False,
    )
    db.session.add(arena_doc)
    db.session.commit()  # ensure arena_doc.id is assigned

    # Create the arena instance.
    arena = Arena(
        arena_id=arena_doc.id,
        new_strategies=strategy_classes,
        existing_strategies=None,
        rounds_per_game=rounds_per_game,
        games_per_pair=games_per_pair,
        points_per_game=max_points,
        max_point_threshold=max_points,
        is_regular=False,
    )

    # Submit the arena run function to the executor.
    executor.submit(run_arena_and_update_runtime, arena, arena_doc.id)

    return {"arena": arena_doc.id}, 202


@bp.get("/<arena_id>")
@onboarding_required
def get_arena(arena_id):
    """
    Retrieves detailed information for a specific Arena.
    Checks if the arena is fully completed. If not, returns progress.
    If completed, returns various analytics (e.g., average scores, win ratios, heatmap data, etc.).
    """

    # 1. Fetch the arena and check existence
    arena = db.session.execute(
        select(ArenaModel).where(
            ArenaModel.id == arena_id, ArenaModel.is_deleted == False
        )
    ).scalar()

    if not arena:
        return {"error": "Not found"}, 404

    # 2. Check progress (completed vs total games)
    completed = len(arena.games)
    total_games = (
        arena.games_per_pair
        * arena.number_strategies
        * (arena.number_strategies - 1)
        / 2
    )

    # If not all games are completed, return only the progress
    if completed != total_games:
        progress = round(completed / total_games, 2) if total_games else 0
        return {"progress": progress}

    # -----------------------
    # HELPER QUERIES & FUNCS
    # -----------------------

    # A. Base "Union" Query (leveraging the new Result model)
    def base_union_query(arena_id: int):
        """
        Constructs a SQLAlchemy query to retrieve all strategies used in games within a specified arena.
        For each strategy, it fetches:
          - Strategy ID      (id)
          - Strategy Score   (score)
          - Opponent Score   (opponent_score)
          - Strategy Name    (name)
          - Author's Name    (author)
        """

        OpponentResult = aliased(ResultModel)

        query = (
            select(
                ResultModel.strategy_id.label("id"),
                ResultModel.score.label("score"),
                OpponentResult.score.label("opponent_score"),
                StrategyModel.name.label("name"),
                UserModel.username.label("author"),
            )
            .select_from(ResultModel)
            .join(StrategyModel, ResultModel.strategy_id == StrategyModel.id)
            .join(UserModel, UserModel.id == StrategyModel.user_id)
            .join(GameModel, ResultModel.game_id == GameModel.id)
            .join(
                OpponentResult,
                and_(
                    OpponentResult.game_id == ResultModel.game_id,
                    OpponentResult.strategy_id == ResultModel.opponent_strategy_id,
                ),
            )
            .where(GameModel.arena_id == arena_id, GameModel.is_deleted == False)
        )

        return query

    # B. Helper function to fetch data from a query and return list of dicts
    def fetch_game_data(query):
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    # --------------------------
    # 1) AVERAGE SCORES (Bar Plot)
    # --------------------------
    def get_average_scores(arena_id: int):
        """
        Retrieves the average score for each strategy within a specified arena.
        """
        # Use the base_union_query as a subquery
        union_subquery = base_union_query(arena_id).subquery()

        avg_scores_query = (
            select(
                union_subquery.c.id,
                union_subquery.c.name,
                union_subquery.c.author,
                func.avg(union_subquery.c.score).label("avg_score"),
            )
            .group_by(
                union_subquery.c.id, union_subquery.c.name, union_subquery.c.author
            )
            .order_by(desc("avg_score"))
        )

        rows = db.session.execute(avg_scores_query).all()
        return [
            {
                "id": row.id,
                "name": row.name,
                "author": row.author,
                "avg_score": float(row.avg_score),
            }
            for row in rows
        ]

    # ------------------------------------
    # 2) WIN RATIOS (Score > Opponent’s)
    # ------------------------------------
    def get_win_ratios(arena_id: int) -> Dict[int, float]:
        """
        Calculates the win ratio for each strategy within a specified arena.
        The query now self-joins the Result table so each strategy’s score is
        compared with the score of the opponent (found in the opposing result row).
        """
        # Create an alias for the opponent result row
        OppResult = aliased(ResultModel)

        ratio_query = (
            select(
                ResultModel.strategy_id.label("strategy_id"),
                func.count().label("total_games"),
                func.sum(
                    case(
                        (ResultModel.score > OppResult.score, 1),
                        else_=0,
                    )
                ).label("wins"),
            )
            # Join the Game model to filter by arena_id and non-deleted games.
            .join(GameModel, ResultModel.game_id == GameModel.id)
            # Self-join the Result table to get the opponent's score.
            .join(
                OppResult,
                and_(
                    OppResult.game_id == ResultModel.game_id,
                    # Match the opponent's strategy using the values stored
                    # in the current result row.
                    OppResult.strategy_id == ResultModel.opponent_strategy_id,
                    OppResult.opponent_strategy_id == ResultModel.strategy_id,
                ),
            )
            .where(
                GameModel.arena_id == arena_id,
                GameModel.is_deleted
                == False,  # adjust according to your actual deletion field
            )
            .group_by(ResultModel.strategy_id)
        )

        result = db.session.execute(ratio_query).all()

        # Calculate win ratios per strategy
        win_ratios = {}
        for row in result:
            strategy_id = row.strategy_id
            total_games = row.total_games
            wins = row.wins or 0
            win_ratio = wins / total_games if total_games else 0
            win_ratios[strategy_id] = win_ratio

        return win_ratios

    # --------------------------
    # 3) ALL SCORES (Box Plot)
    # --------------------------
    def get_all_scores(arena_id: int) -> List[Dict]:
        """
        Retrieves all scores for each strategy within a specified arena.
        """
        union_subquery = base_union_query(arena_id).subquery()

        all_scores_query = select(
            union_subquery.c.id,
            union_subquery.c.name,
            union_subquery.c.author,
            union_subquery.c.score,
        )

        rows = db.session.execute(all_scores_query).all()
        return [
            {
                "id": row.id,
                "name": row.name,
                "author": row.author,
                "score": float(row.score),
            }
            for row in rows
        ]

    # ----------------------------------------------
    # 4) HEATMAP DATA (Strategy vs. Strategy Scores)
    # ----------------------------------------------
    def get_strategy_vs_strategy_scores(arena_id: int):
        """
        Returns heat-map records of
          • strategy1_id, strategy1_name
          • strategy2_id, strategy2_name
          • strategy1_avg  (avg score of strategy 1 against strategy 2)
          • strategy2_avg  (avg score of strategy 2 against strategy 1)
        One row per (strategy-A, strategy-B) pair for the given arena.
        """
        OpponentResult = aliased(ResultModel)
        Strat1 = aliased(StrategyModel)
        Strat2 = aliased(StrategyModel)

        heatmap_query = (
            select(
                ResultModel.strategy_id.label("strategy1_id"),
                Strat1.name.label("strategy1_name"),
                OpponentResult.strategy_id.label("strategy2_id"),
                Strat2.name.label("strategy2_name"),
                func.avg(ResultModel.score).label("strategy1_avg"),
                func.avg(OpponentResult.score).label("strategy2_avg"),
            )
            # join Game row → filter by arena
            .join(GameModel, ResultModel.game_id == GameModel.id)
            # join the “other side” of the same game
            .join(
                OpponentResult,
                and_(
                    OpponentResult.game_id == ResultModel.game_id,
                    OpponentResult.strategy_id == ResultModel.opponent_strategy_id,
                ),
            )
            # join names for both strategies
            .join(Strat1, Strat1.id == ResultModel.strategy_id)
            .join(Strat2, Strat2.id == OpponentResult.strategy_id)
            .where(GameModel.arena_id == arena_id, GameModel.is_deleted == 0)
            .group_by(
                ResultModel.strategy_id,
                Strat1.name,
                OpponentResult.strategy_id,
                Strat2.name,
            )
        )

        return fetch_game_data(heatmap_query)

    # --------------------------------
    # 5) SCORES BY ROUND (Scatter Plot)
    # --------------------------------
    def get_scores_by_round(arena_id: int):
        """
        Returns scores by round for each strategy in the specified arena.
        """
        scores_by_round_query = (
            select(
                GameModel.game_number.label("round"),
                ResultModel.strategy_id.label("id"),
                StrategyModel.name.label("name"),
                ResultModel.score.label("score"),
            )
            .join(GameModel, ResultModel.game_id == GameModel.id)
            .join(StrategyModel, ResultModel.strategy_id == StrategyModel.id)
            .where(GameModel.arena_id == arena_id, GameModel.is_deleted == False)
            .order_by(GameModel.game_number)
        )
        return fetch_game_data(scores_by_round_query)

    # ---------------------
    # ASSEMBLE THE RESPONSE
    # ---------------------

    # At this point, we've confirmed that the Arena is complete.
    # You can now fetch and return whichever analytics you want:
    average_scores = get_average_scores(arena_id)
    win_ratios = get_win_ratios(arena_id)
    all_scores = get_all_scores(arena_id)
    heatmap_data = get_strategy_vs_strategy_scores(arena_id)
    scores_by_round = get_scores_by_round(arena_id)

    return {
        "average_scores": average_scores,
        "win_ratios": win_ratios,
        "all_scores": all_scores,
        "heatmap_data": heatmap_data,
        "scores_by_round": scores_by_round,
    }


@bp.get("/<int:arena_id>/games")
@onboarding_required
def get_arena_games(arena_id: int):
    """
    GET /arenas/{arena_id}/games
    For a given arena, return for each participating strategy:
      - its name
      - its author
      - the list of per‐game scores it earned in that arena
    """
    # 1) verify arena exists & is accessible
    arena = (
        db.session.query(ArenaModel)
        .filter(
            ArenaModel.id == arena_id,
            ArenaModel.is_deleted == False,
            # you can add visibility checks here if needed
        )
        .first()
    )
    if not arena:
        abort(404, description="Arena not found.")

    # 2) alias models for clarity
    Strat = aliased(StrategyModel)
    Auth = aliased(UserModel)

    # 3) query: pull every Result.score for each strategy in this arena
    rows = (
        db.session.execute(
            select(
                ResultModel.strategy_id.label("strategy_id"),
                Strat.name.label("strategy_name"),
                Auth.name.label("author_name"),
                ResultModel.score.label("score"),
            )
            .join(GameModel, ResultModel.game_id == GameModel.id)
            .join(Strat, Strat.id == ResultModel.strategy_id)
            .join(Auth, Auth.id == Strat.user_id)
            .where(
                GameModel.arena_id == arena_id,
                ResultModel.is_deleted == False,
                Strat.is_deleted == False,
            )
            .order_by(ResultModel.strategy_id, GameModel.game_number)
        )
        .mappings()
        .all()
    )

    # 4) aggregate into per‐strategy buckets
    StrategyDetails = TypedDict(
        "StrategyDetails",
        {
            "name": str,
            "author": str,
            "scores": List[float],
        },
    )
    games_by_strategy: Dict[int, StrategyDetails] = {}

    for row in rows:
        sid = row["strategy_id"]
        if sid not in games_by_strategy:
            games_by_strategy[sid] = {
                "name": row["strategy_name"],
                "author": row["author_name"],
                "scores": [],
            }
        games_by_strategy[sid]["scores"].append(row["score"])

    # 5) return JSON
    return jsonify(games_by_strategy)


@bp.get("/leaderboard")
# @onboarding_required
def get_leaderboard():
    # 0) identify current user
    """
    user_header = json.loads(request.headers.get("X-User"))
    me = db.session.execute(
        select(UserModel).where(UserModel.oauth_email == user_header["email"])
    ).scalar()
    if not me:
        return {"error": "User not found"}, 404
    """
    # 1) For every strategy-vs-opponent pair in regular arenas, find the last arena_id
    last_pairing_arena = (
        select(
            ResultModel.strategy_id.label("sid"),
            ResultModel.opponent_strategy_id.label("oid"),
            func.max(GameModel.arena_id).label("last_arena_id"),
        )
        .join(GameModel, ResultModel.game_id == GameModel.id)
        .join(ArenaModel, GameModel.arena_id == ArenaModel.id)
        .where(
            ArenaModel.is_regular == 1,
            ArenaModel.games_played > 0,
        )
        .group_by(ResultModel.strategy_id, ResultModel.opponent_strategy_id)
        .subquery()
    )

    # 2) From that, grab the Result rows that actually belong to those “last arenas”
    last_results = (
        select(ResultModel.strategy_id, ResultModel.score)
        .select_from(ResultModel)
        .join(
            last_pairing_arena,
            and_(
                ResultModel.strategy_id == last_pairing_arena.c.sid,
                ResultModel.opponent_strategy_id == last_pairing_arena.c.oid,
            ),
        )
        .join(GameModel, ResultModel.game_id == GameModel.id)
        .where(GameModel.arena_id == last_pairing_arena.c.last_arena_id)
        .subquery()
    )

    # 3) Compute average points per strategy over those “last-match” results
    avg_subq = (
        select(
            last_results.c.strategy_id,
            func.avg(last_results.c.score).label("avg_point"),
        )
        .group_by(last_results.c.strategy_id)
        .subquery()
    )

    # 4) Now build the leaderboard: all strategies not owned by me,
    #    joined to their avg (0 if no matches), author, and has_model flag
    leaderboard_q = (
        select(
            StrategyModel.id.label("strategy_id"),
            StrategyModel.name.label("strategy_name"),
            UserModel.username.label("author"),
            func.coalesce(avg_subq.c.avg_point, 0).label("avg_point_per_game"),
            case((MLModel.id.is_not(None), "yes"), else_="no").label("has_model"),
        )
        .select_from(StrategyModel)
        .join(UserModel, StrategyModel.user_id == UserModel.id)
        .outerjoin(avg_subq, StrategyModel.id == avg_subq.c.strategy_id)
        .outerjoin(MLModel, MLModel.strategy_id == StrategyModel.id)
        .where(
            StrategyModel.is_deleted == 0,
        )
        .order_by(desc("avg_point_per_game"))
    )

    rows = db.session.execute(leaderboard_q).all()

    leaderboard = [
        {
            "id": r.strategy_id,
            "strategy_name": r.strategy_name,
            "author": r.author,
            "avg_point_per_game": float(r.avg_point_per_game),
            "has_model": r.has_model,
        }
        for r in rows
    ]

    return jsonify({"leaderboard": leaderboard})
