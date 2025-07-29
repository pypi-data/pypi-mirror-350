# SPDX‑License‑Identifier: MIT
"""Improved, safer and faster replacement for the original **arena.py**.

Key improvements
----------------
* **Streamed model downloads + automatic cleanup** – avoids RAM spikes and disk
  litter (temp files are removed at process exit).
* **Model caching** – TensorFlow, TorchScript & ONNX models are loaded **once**
  via an LRU cache and then reused; no per‑game reloads.
* **One `Game` instance per pair** – strategies (and therefore their models)
  are constructed a single time per pair, not for every game‑round.
* **Secure loading pipeline** – only allows “safe” model formats and disables
  arbitrary object deserialisation.
* **Smaller public API for strategy authors** – constructors may accept either
  a `model` object or nothing; legacy “model_path” still works.
"""
from __future__ import annotations

import itertools
import logging
import os
import pathlib
import tempfile
import time
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Final, List, Tuple, Type, Literal, Optional, Dict, Any
import rpsa_sdk

import importlib.util

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

# ────────────────────────────────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────────────────────────────────
OPTIONS = Literal["rock", "paper", "scissors"]
_STR_TO_INT: Final[Dict[str, int]] = {"rock": 0, "paper": 1, "scissors": 2}
_VALID_MOVES: Final = frozenset(_STR_TO_INT)
_NO_POINT_THRESHOLD: Final = 0.001

_ALLOWED_MODEL_EXT: Final = {".ts", ".onnx", ".h5", ".pb"}
_TEMP_DIR = tempfile.TemporaryDirectory(prefix="arena_models_")
logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────────────────────
# Tiny helpers
# ────────────────────────────────────────────────────────────────────────────


def _winner_mod3(a: int, b: int) -> int:
    """Return 0=tie, 1=a wins, 2=b wins using modulo arith."""
    return (a - b) % 3


def _chunked(
    dst: pathlib.Path, blob_client, chunk_size: int = 4 * 2**20
) -> pathlib.Path:
    """Stream the blob into *dst* path and return the path."""
    with dst.open("wb") as fh:
        stream = blob_client.download_blob()
        # .chunks() in Azure Blob Storage v12+ no longer takes an argument
        for chunk in stream.chunks():
            fh.write(chunk)
    return dst


# ────────────────────────────────────────────────────────────────────────────
# Strategy contract (unchanged)
# ────────────────────────────────────────────────────────────────────────────
class Strategy(ABC):
    name: str
    author: str

    def __init__(self, model: Any | None = None):
        """Implementors may accept a ready‑to‑use *model* or ignore it."""

    @abstractmethod
    def play(self) -> OPTIONS: ...

    @abstractmethod
    def handle_moves(self, own_move: OPTIONS, opponent_move: OPTIONS) -> None: ...


# ────────────────────────────────────────────────────────────────────────────
# Model loaders (LRU‑cached)
# ────────────────────────────────────────────────────────────────────────────
try:
    import tensorflow as _tf  # type: ignore
except ImportError:  # pragma: no cover – optional dep
    _tf = None

try:
    import torch  # type: ignore
except ImportError:  # pragma: no cover – optional dep
    torch = None

try:
    import onnxruntime as _ort  # type: ignore
except ImportError:  # pragma: no cover – optional dep
    _ort = None


def _detect_backend(path: pathlib.Path) -> str:
    ext = path.suffix.lower()
    if ext in {".ts", ".pt"}:
        return "torch"
    if ext in {".pb", ".h5"}:
        return "tf"
    if ext == ".onnx":
        return "onnx"
    raise ValueError(f"Unsupported model extension: {ext}")


@lru_cache(maxsize=None)
def _load_model(path: str):  # noqa: ANN001 – generic loader
    p = pathlib.Path(path)
    backend = _detect_backend(p)

    if backend == "torch":
        if torch is None:
            raise RuntimeError("PyTorch not available at runtime")
        return torch.jit.load(str(p), map_location="cpu")

    if backend == "tf":
        if _tf is None:
            raise RuntimeError("TensorFlow not available at runtime")
        return _tf.keras.models.load_model(str(p), compile=False)

    if backend == "onnx":
        if _ort is None:
            raise RuntimeError("ONNX Runtime missing")
        return _ort.InferenceSession(str(p), providers=["CPUExecutionProvider"])

    # should never reach here
    raise AssertionError(backend)


# ────────────────────────────────────────────────────────────────────────────
# One N‑round game between two **Strategy *instances*** (micro‑optimised)
# ────────────────────────────────────────────────────────────────────────────
class Game:
    __slots__ = (
        "strategy1",
        "strategy2",
        "_play1",
        "_play2",
        "_handle1",
        "_handle2",
    )

    def __init__(self, strat1: Strategy, strat2: Strategy) -> None:
        self.strategy1 = strat1
        self.strategy2 = strat2
        self._play1 = strat1.play
        self._play2 = strat2.play
        self._handle1 = strat1.handle_moves
        self._handle2 = strat2.handle_moves

    # no internal counters – caller keeps score
    def play_rounds(self, n: int) -> Tuple[int, int, int]:
        win1 = win2 = tie = 0
        play1, play2 = self._play1, self._play2
        handle1, handle2 = self._handle1, self._handle2
        str_to_int = _STR_TO_INT

        for i in range(n):
            c1 = play1()
            c2 = play2()

            try:
                i1 = str_to_int[c1]
                i2 = str_to_int[c2]
            except KeyError as bad:
                raise ValueError(f"Invalid move: {bad.args[0]!r} vs {c2!r}")

            handle1(c1, c2)
            handle2(c2, c1)

            diff = _winner_mod3(i1, i2)
            if diff == 0:
                tie += 1
            elif diff == 1:
                win1 += 1
            else:
                win2 += 1

        return win1, win2, tie


# ────────────────────────────────────────────────────────────────────────────
# Arena runner (pairs logic & model pipeline rewritten)
# ────────────────────────────────────────────────────────────────────────────
class Arena:
    def __init__(
        self,
        arena_id: int,
        new_strategies: List[Type[Strategy]],
        existing_strategies: Optional[List[Type[Strategy]]] = None,
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

        # ── DB sanity ────────────────────────────────────────────────────
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

        # ── Load or download ML models only once ─────────────────────────
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
                    suffix = pathlib.Path(ml.filename).suffix.lower()
                    if suffix not in _ALLOWED_MODEL_EXT:
                        logger.warning(
                            "Refusing download of unsupported model '%s'", ml.filename
                        )
                        continue

                    dst_path = pathlib.Path(_TEMP_DIR.name) / ml.filename
                    try:
                        _chunked(dst_path, blob_ctr.get_blob_client(ml.path))
                    except Exception as exc:  # pragma: no cover – network I/O
                        logger.error("Failed to download %s: %s", ml.filename, exc)
                        continue
                    self._model_paths[strat_name] = str(dst_path)
                else:
                    logger.warning("No blob client for model%s", ml.filename)

        # ── Pair matrix (unchanged) ──────────────────────────────────────
        if is_regular:
            new_vs_new = list(itertools.combinations(new_strategies, 2))
            new_vs_old = [
                (new_s, old_s)
                for new_s in new_strategies
                for old_s in (existing_strategies or [])
            ]
            self._pairs = new_vs_new + new_vs_old
        else:
            self._pairs = list(itertools.combinations(new_strategies, 2))

        self._games_played = 0
        self._total_runtime = 0.0

    # ────────────────────────────────────────────────────────────────────
    # Public API
    # ────────────────────────────────────────────────────────────────────
    def start(self) -> None:  # noqa: C901 – top‑level coordinator
        try:
            self._run_pairs()
            self._persist_stats()
            if self.is_regular:
                self._mark_participated([s.name for s in self._pairs_flat()])
        except Exception:  # pragma: no cover – outermost guard
            self.session.rollback()
            logger.exception("Arena run failed")
            raise
        finally:
            self.session.close()

    # ────────────────────────────────────────────────────────────────────
    # Internal helpers
    # ────────────────────────────────────────────────────────────────────
    def _instantiate_strategy(self, cls: Type[Strategy]) -> Strategy:
        """Create one instance of *cls* with a *cached* model object if available."""
        model_path = self._model_paths.get(cls.name)
        if model_path:
            try:
                model_obj = _load_model(model_path)
            except Exception as exc:  # pragma: no cover – corrupted files etc.
                logger.error("Cannot load model for %s: %s", cls.name, exc)
                model_obj = None
        else:
            model_obj = None

        # two‑step fallback: (1) try constructor(model)  (2) constructor()
        try:
            return cls(model_obj)
        except TypeError:
            # legacy strategy expecting a *path* – still give the cached path
            return cls(model_path) if model_path else cls()

    # ------------------------------------------------------------------
    def _run_pairs(self) -> None:
        strat_id = self.strategy_id_map
        rounds = self.rounds_per_game
        games_per_pair = self.games_per_pair

        # Pre‑build reusable Game objects (1 per pair) -------------------
        game_objs: List[Tuple[Game, Type[Strategy], Type[Strategy]]] = []
        for s1_cls, s2_cls in self._pairs:
            g = Game(
                self._instantiate_strategy(s1_cls), self._instantiate_strategy(s2_cls)
            )
            game_objs.append((g, s1_cls, s2_cls))

        # Buffers for DB bulk insert ------------------------------------
        games_buf: List[GameModel] = []
        results_buf: List[Tuple[int, int, int, int, int]] = []

        for game_no in range(1, games_per_pair + 1):
            for g, s1_cls, s2_cls in game_objs:
                t0 = time.perf_counter()
                try:
                    w1, w2, ties = g.play_rounds(rounds)
                except Exception as exc:
                    logger.error(
                        "Error in game %s vs %s: %s", s1_cls.name, s2_cls.name, exc
                    )
                    continue
                runtime = time.perf_counter() - t0

                gm = GameModel(
                    arena_id=self.arena.id,
                    game_number=game_no,
                    runtime=runtime,
                    strategy_a_id=strat_id[s1_cls.name],
                    strategy_b_id=strat_id[s2_cls.name],
                    wins_a=w1,
                    wins_b=w2,
                    ties=ties,
                    total_rounds=rounds,
                )
                games_buf.append(gm)
                results_buf.append(
                    (w1, w2, ties, strat_id[s1_cls.name], strat_id[s2_cls.name])
                )

                self._games_played += 1
                self._total_runtime += runtime

        # ── Bulk‑commit games and results -------------------------------
        self.session.bulk_save_objects(games_buf, return_defaults=True)
        self.session.flush()

        self._persist_results(games_buf, results_buf)

    # ------------------------------------------------------------------
    def _persist_results(
        self, games: List[GameModel], res_buf: List[Tuple[int, int, int, int, int]]
    ) -> None:
        result_objs: List[ResultModel] = []
        max_pts = self.max_points_per_game
        max_thr = self.max_point_threshold
        no_pts = _NO_POINT_THRESHOLD

        for gm, (w1, w2, ties, id1, id2) in zip(games, res_buf):
            non_ties = w1 + w2 or 1
            if (w1 + w2) <= ties or abs(w1 - w2) < non_ties * no_pts:
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

    # ------------------------------------------------------------------
    def _persist_stats(self) -> None:
        if not self._games_played:
            return
        self.session.query(ArenaModel).filter_by(id=self.arena.id).update(
            {
                "games_played": self._games_played,
                "total_rounds": self._games_played * self.rounds_per_game,
                "avg_game_runtime": self._total_runtime / self._games_played,
            }
        )
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


# ensure temp dir is removed on interpreter exit
import atexit

atexit.register(_TEMP_DIR.cleanup)
