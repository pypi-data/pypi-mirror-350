# File: rpsa_backend/public_api/schemas.py

"""
Marshmallow schemas for serialising public-API payloads.
Includes arena-level, game-level, result-level, strategy-level,
head-to-head, and leaderboard schemas.
"""

from marshmallow import Schema, fields


# ────────────────────────────────────────────────────────────────────────────────
# Arena metadata + aggregates
# ────────────────────────────────────────────────────────────────────────────────
class ArenaSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    number_strategies = fields.Int()
    rounds_per_game = fields.Int()
    games_per_pair = fields.Int()
    max_points = fields.Int()

    runtime = fields.Float(allow_none=True)
    is_regular = fields.Bool()

    # aggregates
    games_played = fields.Int()
    total_rounds = fields.Int()
    avg_game_runtime = fields.Float(allow_none=True)


# ────────────────────────────────────────────────────────────────────────────────
# Game summary with raw counts
# ────────────────────────────────────────────────────────────────────────────────
class GameSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    game_number = fields.Int()
    runtime = fields.Float(allow_none=True)

    strategy_a_id = fields.Int()
    strategy_b_id = fields.Int()
    wins_a = fields.Int()
    wins_b = fields.Int()
    ties = fields.Int()
    total_rounds = fields.Int()


# ────────────────────────────────────────────────────────────────────────────────
# Per-strategy result row
# ────────────────────────────────────────────────────────────────────────────────
class ResultSchema(Schema):
    strategy_id = fields.Int()
    strategy_name = fields.Method("get_strategy_name")
    opponent_strategy_id = fields.Int()

    # raw counts
    wins = fields.Int()
    losses = fields.Int()
    ties = fields.Int()
    win_rate = fields.Float()
    net_score = fields.Int()

    # normalized arena score
    score = fields.Float()

    def get_strategy_name(self, obj):
        # Lazily resolve the strategy relation
        return getattr(obj.strategy, "module_name", None)


# ────────────────────────────────────────────────────────────────────────────────
# Aggregated strategy summary (per strategy)
# ────────────────────────────────────────────────────────────────────────────────
class StrategySummarySchema(Schema):
    strategy_id = fields.Int()
    strategy_name = fields.Str()
    plays = fields.Int()
    wins = fields.Int()
    losses = fields.Int()
    ties = fields.Int()
    total_score = fields.Float()
    avg_points_per_game = fields.Float()
    games_played = fields.Int()
    net_score = fields.Int()
    win_rate = fields.Float()


# ────────────────────────────────────────────────────────────────────────────────
# Head-to-head matchups between two strategies
# ────────────────────────────────────────────────────────────────────────────────
class MatchupSchema(Schema):
    """
    Head-to-head metrics between two strategies.
    """

    strategy_id = fields.Int()
    opponent_strategy_id = fields.Int()
    wins = fields.Int()
    losses = fields.Int()
    ties = fields.Int()
    net_score = fields.Int()
    win_rate = fields.Float()
    avg_points_per_game = fields.Float()
    games_played = fields.Int()


# ────────────────────────────────────────────────────────────────────────────────
# Per-arena leaderboard of strategies
# ────────────────────────────────────────────────────────────────────────────────
class LeaderboardSchema(Schema):
    strategy_id = fields.Int()
    strategy_name = fields.Str()
    avg_points_per_game = fields.Float()
    games_played = fields.Int()
    wins = fields.Int()
    losses = fields.Int()
    ties = fields.Int()
    net_score = fields.Int()
    win_rate = fields.Float()
