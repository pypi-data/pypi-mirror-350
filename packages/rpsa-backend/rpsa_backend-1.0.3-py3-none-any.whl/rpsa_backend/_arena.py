from __future__ import annotations

import itertools
import logging
import os
import tempfile
import time
from abc import ABC, abstractmethod
from typing import Final, List, Tuple, Type, Literal, Optional, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from azure.storage.blob import BlobServiceClient

from . import db
from .models import (
    Arena as ArenaModel,
    Game as GameModel,
    Result as ResultModel,
    Strategy as StrategyModel,
    MLModel,
)

# ───────────────────────────────────────────────────────────────────────────────
# Shared constants – moved to module level for speed
# ───────────────────────────────────────────────────────────────────────────────
OPTIONS = Literal["rock", "paper", "scissors"]
_STR_TO_INT: Final[Dict[str, int]] = {"rock": 0, "paper": 1, "scissors": 2}
_VALID_MOVES: Final = frozenset(_STR_TO_INT)
_NO_POINT_THRESHOLD: Final = 0.001

logger = logging.getLogger(__name__)


# ───────────────────────────────────────────────────────────────────────────────
# Strategy contract (unchanged)
# ───────────────────────────────────────────────────────────────────────────────
class Strategy(ABC):
    name: str
    author: str

    @abstractmethod
    def play(self) -> OPTIONS: ...

    @abstractmethod
    def handle_moves(self, own_move: OPTIONS, opponent_move: OPTIONS) -> None: ...


# ───────────────────────────────────────────────────────────────────────────────
# One 2 000‐round game between two Strategy classes – micro-optimised
# ───────────────────────────────────────────────────────────────────────────────
class Game:
    __slots__ = (
        "strategy1",
        "strategy2",
        "win1",
        "win2",
        "tie",
        "_play1",
        "_play2",
        "_handle1",
        "_handle2",
    )

    def __init__(
        self,
        strat1_cls: Type[Strategy],
        strat2_cls: Type[Strategy],
        model_paths: dict[str, str],
    ) -> None:
        self.strategy1 = (
            strat1_cls(model_paths.get(strat1_cls.name))
            if model_paths.get(strat1_cls.name)
            else strat1_cls()
        )
        self.strategy2 = (
            strat2_cls(model_paths.get(strat2_cls.name))
            if model_paths.get(strat2_cls.name)
            else strat2_cls()
        )

        self._play1 = self.strategy1.play
        self._play2 = self.strategy2.play
        self._handle1 = self.strategy1.handle_moves
        self._handle2 = self.strategy2.handle_moves

        self.win1 = self.win2 = self.tie = 0

    def play_rounds(self, n: int) -> Tuple[int, int, int]:
        win1 = win2 = tie = 0

        play1, play2 = self._play1, self._play2
        handle1, handle2 = self._handle1, self._handle2
        str_to_int = _STR_TO_INT
        winner_mod3 = lambda a, b: (a - b) % 3

        for _ in range(n):
            c1 = play1()
            c2 = play2()

            try:
                i1 = str_to_int[c1]
                i2 = str_to_int[c2]
            except KeyError as bad:
                raise ValueError(f"Invalid move: {bad.args[0]!r} vs {c2!r}") from None

            handle1(c1, c2)
            handle2(c2, c1)

            diff = winner_mod3(i1, i2)
            if diff == 0:
                tie += 1
            elif diff == 1:
                win1 += 1
            else:
                win2 += 1

        self.win1, self.win2, self.tie = win1, win2, tie
        return win1, win2, tie

    @staticmethod
    def _winner(i1: int, i2: int) -> int:
        return (i1 - i2) % 3


# ───────────────────────────────────────────────────────────────────────────────
# Arena runner (only _pairs logic changed)
# ───────────────────────────────────────────────────────────────────────────────
class Arena:
    def __init__(
        self,
        arena_id: int,
        new_strategies: List[Type[StrategyModel]],
        existing_strategies: Optional[List[Type[StrategyModel]]] = None,
        rounds_per_game: int = 100,
        games_per_pair: int = 10,
        points_per_game: float = 1.0,
        max_point_threshold: float = 1.0,
        is_regular: bool = True,
    ) -> None:
        self.arena_id = arena_id
        self.rounds_per_game = rounds_per_game
        self.games_per_pair = games_per_pair
        self.max_points_per_game = points_per_game
        self.max_point_threshold = max_point_threshold
        self.is_regular = is_regular

        self.session: Session = db.session

        self.arena: ArenaModel = (
            self.session.execute(
                select(ArenaModel).where(
                    ArenaModel.id == arena_id, ArenaModel.is_deleted == 0
                )
            )
            .scalars()
            .one_or_none()
        )
        if not self.arena:
            raise ValueError(f"No active Arena with id={arena_id}")

        combined = (
            new_strategies + (existing_strategies or [])
            if is_regular
            else new_strategies
        )
        rows = (
            self.session.execute(
                select(StrategyModel).where(
                    StrategyModel.name.in_(cls.name for cls in combined),
                    StrategyModel.is_deleted == 0,
                )
            )
            .scalars()
            .all()
        )
        self.strategy_id_map: Dict[str, int] = {s.name: s.id for s in rows}
        missing = {cls.name for cls in combined} - self.strategy_id_map.keys()
        if missing:
            raise ValueError(f"Strategies missing in DB: {missing}")

        # ML models loading (unchanged) …
        self._model_paths: Dict[str, str] = {}
        ml_rows = (
            self.session.execute(
                select(MLModel).where(
                    MLModel.strategy_id.in_(self.strategy_id_map.values()),
                    MLModel.is_deleted == 0,
                )
            )
            .scalars()
            .all()
        )
        if ml_rows:
            blob_conn = os.getenv("BLOB_CONN_STRING")
            blob_container = os.getenv("BLOB_CONTAINER")
            blob_ctr = (
                BlobServiceClient.from_connection_string(
                    blob_conn
                ).get_container_client(blob_container)
                if blob_conn and blob_container
                else None
            )

            for ml in ml_rows:
                strat_name = next(
                    k for k, v in self.strategy_id_map.items() if v == ml.strategy_id
                )
                if ml.storage == "local":
                    self._model_paths[strat_name] = ml.path
                elif blob_ctr:
                    data = blob_ctr.get_blob_client(ml.path).download_blob().readall()
                    suffix = os.path.splitext(ml.filename)[1]
                    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
                    tmp.write(data)
                    tmp.flush()
                    self._model_paths[strat_name] = tmp.name
                else:
                    logger.warning("No blob client for model %s", ml.filename)

        self._games_played = 0
        self._total_runtime = 0.0

        # ── Here's the only change: build exactly the right pairs ──────────────
        if is_regular:
            # 1) new vs new (each pair once)
            new_vs_new = list(itertools.combinations(new_strategies, 2))
            # 2) new vs existing
            new_vs_old = [
                (new_s, old_s)
                for new_s in new_strategies
                for old_s in (existing_strategies or [])
            ]
            self._pairs = new_vs_new + new_vs_old
        else:
            # pure all-vs-all among new_strategies
            self._pairs = list(itertools.combinations(new_strategies, 2))

    def start(self) -> None:
        try:
            self._run_pairs(self._pairs)

            if self._games_played:
                self.session.query(ArenaModel).filter_by(id=self.arena.id).update(
                    {
                        "games_played": self._games_played,
                        "total_rounds": self._games_played * self.rounds_per_game,
                        "avg_game_runtime": self._total_runtime / self._games_played,
                    }
                )
                self.session.commit()

            if self.is_regular:
                self._mark_participated([s.name for s in self._pairs_flat()])

        except Exception:
            self.session.rollback()
            logger.exception("Arena run failed")
            raise
        finally:
            self.session.close()

    def _run_pairs(self, pairs) -> None:
        games_buf: List[GameModel] = []
        results_buf: List[Tuple[int, int, int, int, int]] = []

        strat_id = self.strategy_id_map
        model_paths = self._model_paths
        rounds = self.rounds_per_game
        games_per_pair = self.games_per_pair

        for game_no in range(1, games_per_pair + 1):
            for s1, s2 in pairs:
                t0 = time.perf_counter()
                g = Game(s1, s2, model_paths)
                try:
                    w1, w2, ties = g.play_rounds(rounds)
                except Exception as exc:
                    logger.error("Error in game %s vs %s: %s", s1.name, s2.name, exc)
                    continue
                runtime = time.perf_counter() - t0

                gm = GameModel(
                    arena_id=self.arena.id,
                    game_number=game_no,
                    runtime=runtime,
                    strategy_a_id=strat_id[s1.name],
                    strategy_b_id=strat_id[s2.name],
                    wins_a=w1,
                    wins_b=w2,
                    ties=ties,
                    total_rounds=rounds,
                )
                games_buf.append(gm)
                results_buf.append((w1, w2, ties, strat_id[s1.name], strat_id[s2.name]))

                self._games_played += 1
                self._total_runtime += runtime

        self.session.bulk_save_objects(games_buf, return_defaults=True)
        self.session.flush()

        result_objs: List[ResultModel] = []
        max_pts = self.max_points_per_game
        max_thr = self.max_point_threshold
        no_pts = _NO_POINT_THRESHOLD

        for gm, (w1, w2, ties, id1, id2) in zip(games_buf, results_buf):
            non_ties = w1 + w2
            if non_ties <= ties or abs(w1 - w2) < non_ties * no_pts:
                s1 = s2 = 0.0
            else:
                s1 = (
                    max(min(((w1 / non_ties) - 0.5) / (max_thr - 0.5), 1.0), -1.0)
                    * max_pts
                )
                s2 = (
                    max(min(((w2 / non_ties) - 0.5) / (max_thr - 0.5), 1.0), -1.0)
                    * max_pts
                )

            non_ties = non_ties or 1
            result_objs.extend(
                (
                    ResultModel(
                        game_id=gm.id,
                        strategy_id=id1,
                        opponent_strategy_id=id2,
                        score=s1,
                        wins=w1,
                        losses=w2,
                        ties=ties,
                        win_rate=w1 / non_ties,
                        net_score=w1 - w2,
                    ),
                    ResultModel(
                        game_id=gm.id,
                        strategy_id=id2,
                        opponent_strategy_id=id1,
                        score=s2,
                        wins=w2,
                        losses=w1,
                        ties=ties,
                        win_rate=w2 / non_ties,
                        net_score=w2 - w1,
                    ),
                )
            )

        self.session.bulk_save_objects(result_objs)
        self.session.commit()

    def _pairs_flat(self):
        for a, b in self._pairs:
            yield a
            yield b

    def _mark_participated(self, names):
        ids = [self.strategy_id_map[n] for n in names]
        (
            self.session.query(StrategyModel)
            .filter(StrategyModel.id.in_(ids))
            .update(
                {StrategyModel.has_participated_in_contest: True},
                synchronize_session=False,
            )
        )
        self.session.commit()
