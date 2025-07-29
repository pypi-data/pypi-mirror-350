from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import (
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    UniqueConstraint,
    Table,
    Column,
    DDL,
    event,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db


# ────────────────────────────────────────────────────────────────────────────────
# Base
# ────────────────────────────────────────────────────────────────────────────────
class BaseModel(db.Model):
    """
    BaseModel provides common fields for all models:
    - created_at: Timestamp for when the record was created.
    - is_deleted: Soft-delete flag.
    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


# ────────────────────────────────────────────────────────────────────────────────
# User & auth
# ────────────────────────────────────────────────────────────────────────────────
class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    oauth_email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Profile extras
    born_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    python_knowledge: Mapped[str] = mapped_column(
        String(50), default="entry level", nullable=False
    )
    registered_to_newsletter: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    strategies: Mapped[List["Strategy"]] = relationship(back_populates="user")
    api_keys: Mapped[List["ApiKey"]] = relationship("ApiKey", back_populates="user")
    arenas: Mapped[List["Arena"]] = relationship(
        "Arena", back_populates="user", passive_deletes=True
    )


class ApiKey(BaseModel):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship("User", back_populates="api_keys")


# ────────────────────────────────────────────────────────────────────────────────
# Strategy / ML model
# ────────────────────────────────────────────────────────────────────────────────
class MLModel(BaseModel):
    __tablename__ = "ml_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    strategy_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("strategy.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage: Mapped[str] = mapped_column(String(10), nullable=False)  # 'local'|'blob'
    path: Mapped[str] = mapped_column(String(512), nullable=False)

    strategy: Mapped["Strategy"] = relationship(
        "Strategy", back_populates="model", uselist=False
    )


class Strategy(BaseModel):
    __tablename__ = "strategy"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    module_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="NO ACTION"),
        nullable=False,
        index=True,
    )
    has_participated_in_contest: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    test_runtime: Mapped[Optional[float]] = mapped_column(Float)

    user: Mapped["User"] = relationship(back_populates="strategies")
    model: Mapped[Optional[MLModel]] = relationship(
        "MLModel", back_populates="strategy", uselist=False
    )


# ────────────────────────────────────────────────────────────────────────────────
# Arena & competition
# ────────────────────────────────────────────────────────────────────────────────
class Arena(BaseModel):
    """
    Represents an arena where games are played.
    """

    __tablename__ = "arena"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    number_strategies: Mapped[int] = mapped_column(Integer, nullable=False)
    rounds_per_game: Mapped[int] = mapped_column(Integer, nullable=False)
    games_per_pair: Mapped[int] = mapped_column(Integer, nullable=False)
    max_points: Mapped[int] = mapped_column(Integer, nullable=False)
    is_regular: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    runtime: Mapped[Optional[float]] = mapped_column(Float)

    # NEW → aggregate analytics
    games_played: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_rounds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_game_runtime: Mapped[Optional[float]] = mapped_column(Float)

    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="arenas", passive_deletes=True
    )
    games: Mapped[List["Game"]] = relationship(
        back_populates="arena", cascade="all, delete-orphan"
    )


class Game(BaseModel):
    """
    One 2 000‑round “game” (100 such games = one match‑pair).
    """

    __tablename__ = "game"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    arena_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("arena.id", ondelete="NO ACTION"),
        nullable=False,
        index=True,
    )
    game_number: Mapped[int] = mapped_column(Integer, nullable=False)
    runtime: Mapped[Optional[float]] = mapped_column(Float)

    # NEW → identify the pair and raw outcome
    strategy_a_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("strategy.id"), nullable=False, index=True
    )
    strategy_b_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("strategy.id"), nullable=False, index=True
    )
    wins_a: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wins_b: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_rounds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    arena: Mapped["Arena"] = relationship(back_populates="games")
    results: Mapped[List["Result"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )

    # optional helpers
    strategy_a: Mapped["Strategy"] = relationship(
        "Strategy", foreign_keys=[strategy_a_id], viewonly=True
    )
    strategy_b: Mapped["Strategy"] = relationship(
        "Strategy", foreign_keys=[strategy_b_id], viewonly=True
    )


class Result(BaseModel):
    """
    Per‑strategy view of a single Game.
    """

    __tablename__ = "result"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    game_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("game.id"), nullable=False, index=True
    )
    strategy_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("strategy.id"), nullable=False, index=True
    )
    opponent_strategy_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("strategy.id"), nullable=False, index=True
    )

    # existing arena‑scaled score
    score: Mapped[float] = mapped_column(Float, nullable=False)

    # NEW → raw counts and ratios
    wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    win_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    net_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    game: Mapped["Game"] = relationship(back_populates="results")
    strategy: Mapped["Strategy"] = relationship(
        foreign_keys=[strategy_id], passive_deletes=True
    )
    opponent_strategy: Mapped["Strategy"] = relationship(
        foreign_keys=[opponent_strategy_id], passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint("game_id", "strategy_id", name="uq_game_strategy"),
    )


# ────────────────────────────────────────────────────────────────────────────────
# Queues & pre‑computed results (unchanged)
# ────────────────────────────────────────────────────────────────────────────────
class ArenaQueue(BaseModel):
    __tablename__ = "arena_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    strategies: Mapped[str] = mapped_column(String(255), nullable=False)  # JSON string
    rounds_per_game: Mapped[int] = mapped_column(Integer, nullable=False)
    games_per_pair: Mapped[int] = mapped_column(Integer, nullable=False)
    max_points: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)


class ArenaResults(BaseModel):
    __tablename__ = "arena_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    arena_type: Mapped[str] = mapped_column(String(20), nullable=False)
    arena_id: Mapped[Optional[int]] = mapped_column(Integer)
    results: Mapped[str] = mapped_column(String, nullable=False)


# ────────────────────────────────────────────────────────────────────────────────
# Leaderboard View Definition & Mapping
# ────────────────────────────────────────────────────────────────────────────────

# Define a SQLAlchemy Table to map the database view
leaderboard_view = Table(
    "leaderboard_view",
    db.metadata,
    Column("strategy_id", Integer, primary_key=True),
    Column("strategy_name", String(255)),
    Column("author", String(255)),
    Column("has_model", String(3)),
    Column("avg_point_per_game", Float),
)

# Create the view after tables are created
event.listen(
    leaderboard_view,
    "after_create",
    DDL(
        """
        CREATE VIEW leaderboard_view AS
        WITH last_pair AS (
          SELECT
            r.strategy_id,
            r.opponent_strategy_id,
            MAX(g.arena_id) AS last_arena_id
          FROM result r
          JOIN game  g ON r.game_id = g.id
          JOIN arena a ON g.arena_id = a.id
          WHERE a.is_regular = 1
            AND a.games_played > 0
          GROUP BY r.strategy_id, r.opponent_strategy_id
        )
        SELECT
          s.id                         AS strategy_id,
          s.name                       AS strategy_name,
          u.username                   AS author,
          CASE WHEN m.strategy_id IS NOT NULL THEN 'yes' ELSE 'no' END AS has_model,
          AVG(r.score)                 AS avg_point_per_game
        FROM result r
        JOIN game g  ON r.game_id = g.id
        JOIN arena a ON g.arena_id = a.id
        JOIN strategy s ON r.strategy_id = s.id
        JOIN users    u ON s.user_id = u.id
        LEFT JOIN ml_model m ON m.strategy_id = s.id
        JOIN last_pair lp
          ON r.strategy_id          = lp.strategy_id
         AND r.opponent_strategy_id = lp.opponent_strategy_id
         AND g.arena_id             = lp.last_arena_id
        WHERE a.is_regular = 1
          AND a.games_played > 0
        GROUP BY s.id, s.name, u.username, m.strategy_id;
        """
    ),
)

# Drop the view before tables are dropped
event.listen(
    leaderboard_view, "before_drop", DDL("DROP VIEW IF EXISTS leaderboard_view;")
)


# Map the view to an ORM model
class LeaderboardView(db.Model):
    __table__ = leaderboard_view
    __mapper_args__ = {"primary_key": [leaderboard_view.c.strategy_id]}
