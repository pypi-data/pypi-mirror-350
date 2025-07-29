# SPDX-License-Identifier: MIT
"""
validation.py

Validate user-submitted strategies and their optional ML models, in line with
 the new arena_safe_fast pipeline.

1. Import under a sandboxed subset of builtins.
2. Instantiate with a cached model object (TorchScript, ONNX, TF) if the strategy
   supports it.
3. Enforce unique strategy names.
4. Smoke-test via a quick Game against RandomStrategy.
"""
import importlib.util
import time
import logging
from pathlib import Path
from typing import Optional, Type
import traceback

from .safety import (
    SAFE_BUILTINS,
    SAFE_MODULES,
    PYTHON_ERROR_HELPER,
    MAX_STRATEGY_RUNTIME,
)
from .arena import Game, _load_model, _ALLOWED_MODEL_EXT
from .random_strategy import RandomStrategy, MarkovStrategy
from .models import Strategy as StrategyDB
from . import db
import random
from rpsa_sdk.strategy import Strategy


class StrategyValidationError(Exception):
    """
    Raised when a user strategy fails validation. Carries optional suggestions.
    """

    def __init__(self, message: str, suggestions: Optional[list[str]] = None):
        super().__init__(message)
        self.suggestions = suggestions or []

    def __str__(self) -> str:
        return self.args[0]


def get_error_suggestions(error_message: str) -> list[str]:
    """Map common error fragments to user-friendly hints."""
    suggestions: list[str] = []
    for key, hints in PYTHON_ERROR_HELPER.items():
        if key in error_message:
            suggestions.extend(hints)
    return suggestions


def validate_strategy_script(
    *,
    script_path: str,
    model_path: Optional[str] = None,
) -> tuple[Type[StrategyDB], float]:
    """
    1. Loads the user script under SAFE_BUILTINS.
    2. Instantiates the `strategy` with a pre-loaded model object (if given) *only* if
       the constructor supports it.
    3. Checks for a unique .name and runs a quick 200-round smoke-test.
    """
    try:
        # -- 1) sandboxed import --------------------------------------
        spec = importlib.util.spec_from_file_location(
            Path(script_path).stem, script_path
        )
        module = importlib.util.module_from_spec(spec)
        module.__builtins__ = SAFE_BUILTINS
        spec.loader.exec_module(module)

        if not hasattr(module, "strategy"):
            raise StrategyValidationError(
                "Script must define a top-level variable named `strategy`."
            )

        StratCls = module.strategy

        # -- 2) prepare model object ----------------------------------
        model_obj = None
        if model_path:
            ext = Path(model_path).suffix.lower()
            if ext not in _ALLOWED_MODEL_EXT:
                raise StrategyValidationError(
                    f"Model extension '{ext}' is not allowed.",
                    suggestions=[
                        "Export your network to .ts (TorchScript), .onnx, or .h5/SavedModel"
                    ],
                )
            try:
                model_obj = _load_model(model_path)
            except Exception as e:
                raise StrategyValidationError(
                    f"Failed loading model: {e}",
                    suggestions=[
                        "Ensure the file is a valid TorchScript/ONNX/TF model."
                    ],
                )

        # -- 3) instantiate strategy -----------------------------------
        try:
            if model_obj is not None:
                strat_inst = StratCls(model_obj)
            else:
                strat_inst = StratCls()
        except TypeError:
            # Fallback if the strategy __init__ doesn't accept a model
            strat_inst = StratCls()

        # -- 4) unique name constraint ---------------------------------
        if not hasattr(strat_inst, "name"):
            raise StrategyValidationError(
                "Strategy instance has no `.name` attribute.",
                suggestions=["Add a `name` attribute to your Strategy class."],
            )

        if db.session.query(StrategyDB).filter_by(name=strat_inst.name).first():
            raise StrategyValidationError(
                f"A strategy named '{strat_inst.name}' already exists.",
                suggestions=["Choose a different, unique strategy name."],
            )

        # -- 5a) quick smoke-test via Game.play_rounds(2000) ----------
        try:
            test_game_1 = Game(strat_inst, RandomStrategy())
            t0 = time.perf_counter()
            wins, losses, ties = test_game_1.play_rounds(2000)
            elapsed = time.perf_counter() - t0
        except Exception:
            logging.info(traceback.print_exc())

        if (wins + losses + ties) == 0:
            raise StrategyValidationError("Your strategy never returned a valid move.")
        if elapsed > MAX_STRATEGY_RUNTIME:
            raise StrategyValidationError(
                f"Strategy too slow ({elapsed:.3f}s for 2000 rounds); "
                f"max is {MAX_STRATEGY_RUNTIME}s."
            )

        # -- 5b) extended stress-test: manual play/handle for 2000 steps
        moves = ["rock", "paper", "scissors"]
        try:
            for _ in range(2000):
                m = strat_inst.play()
                if m not in moves:
                    raise ValueError(f"Invalid move from play(): {m!r}")
                # simulate a random opponent
                op = random.choice(moves)
                strat_inst.handle_moves(m, op)
        except Exception as e:
            raise StrategyValidationError(f"Error during extended smoke-test: {e}")

        # -- 5c) quick smoke-test via Game.play_rounds(2000) with a strong opponent ----------
        try:
            # instantiate a “smarter” opponent (e.g. Markov‐chain based)
            strong_opp = MarkovStrategy(Strategy)
            t1 = time.perf_counter()
            wins_2, losses_2, ties_2 = Game(strat_inst, strong_opp).play_rounds(2000)
            elapsed2 = time.perf_counter() - t1
        except Exception as e:
            raise StrategyValidationError(
                f"Error during strong‐opponent smoke-test: {e!s}",
                suggestions=[
                    "Double-check your `handle_moves` logic when the opponent adapts to your history.",
                    "Ensure you’re not accumulating unbounded or invalid internal state.",
                ],
            )

        # did we get *any* moves back?
        if (wins_2 + losses_2 + ties_2) == 0:
            raise StrategyValidationError(
                "Your strategy failed to return any valid moves against the adaptive opponent.",
                suggestions=[
                    "Make sure your `play()` always returns one of 'rock','paper','scissors'."
                ],
            )

        return StratCls, elapsed

    except StrategyValidationError:
        # re-raise our known validation errors
        raise
    except ImportError as e:
        msg = str(e)
        raise StrategyValidationError(
            f"ImportError: {msg}. Only modules in {', '.join(SAFE_MODULES)} are allowed.",
            suggestions=["Check your imports for typos or disallowed modules."],
        )
    except Exception as e:
        msg = str(e)
        suggestions = get_error_suggestions(msg)
        raise StrategyValidationError(msg, suggestions=suggestions)
