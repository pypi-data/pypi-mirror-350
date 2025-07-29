import random

from typing import Literal, Any
import random

from rpsa_sdk.strategy import Strategy
from rpsa_sdk.helpers import counter_move


class RandomStrategy:

    name = "RandomStrategy_Base_ToCheck"
    author = "admin"

    def play(self):
        return random.choice(["rock", "paper", "scissors"])

    def handle_moves(self, own, opponent):
        pass


"""
A 1st-order Markov predictor: learns opponent transitions
and plays the counter to the most likely next move.
"""


class MarkovStrategy(Strategy):
    name = "MarkovStrategy_v1"

    def __init__(self, model: Any = None):
        super().__init__(model=model)
        # transitions[last_move][next_move] = count
        self.transitions: dict[str, dict[str, int]] = {}
        self.last_opponent: str | None = None

    def play(self) -> Literal["rock", "paper", "scissors"]:
        if self.last_opponent is None:
            # no data yet → random
            return random.choice(["rock", "paper", "scissors"])

        # get the transition counts from last_opponent
        nxt_counts = self.transitions.get(self.last_opponent, {})
        if not nxt_counts:
            return random.choice(["rock", "paper", "scissors"])

        # most likely next opponent move
        predicted = max(nxt_counts, key=nxt_counts.get)
        return counter_move(predicted)

    def handle_moves(self, own_move: str, opponent_move: str) -> None:
        if self.last_opponent is not None:
            self.transitions.setdefault(self.last_opponent, {}).setdefault(
                opponent_move, 0
            )
            self.transitions[self.last_opponent][opponent_move] += 1
        self.last_opponent = opponent_move
