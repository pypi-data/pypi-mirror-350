# rpsa-backend/rpsa_backend/__init__.py

import logging
import json

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_executor import Executor
from flask_caching import Cache
from flask_limiter import Limiter
from sqlalchemy import MetaData
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import DeclarativeBase
from werkzeug.exceptions import HTTPException

# retry helpers
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


# ------------------------------------------------------------------------
# Base model for naming conventions
# ------------------------------------------------------------------------
class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


# ------------------------------------------------------------------------
# Extension objects (no init_app yet)
# ------------------------------------------------------------------------
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
cors = CORS()
executor = Executor()
cache = Cache()
limiter = Limiter(key_func=lambda: request.headers.get("X-API-KEY", ""))

# ------------------------------------------------------------------------
# Retry decorator for DB‐init
# ------------------------------------------------------------------------
db_init_retry = retry(
    retry=retry_if_exception_type(DBAPIError),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=5, min=5, max=60),
    reraise=True,
)


# ------------------------------------------------------------------------
# Application factory
# ------------------------------------------------------------------------
def create_app():
    app = Flask(__name__, static_folder=None)

    # 1) HTTPException → JSON
    @app.errorhandler(HTTPException)
    def error_handler(error):
        return jsonify({"error": error.name, "details": error.description}), error.code

    # 2) Logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # 3) Strict trailing slash behavior
    app.url_map.strict_slashes = False

    # 4) Load our Config
    from .config import Config as AppConfig

    app.config.from_object(AppConfig)
    logger.debug("Config loaded from AppConfig")
    logger.debug(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    logger.debug(f"STRATEGY_SOURCE: {app.config.get('STRATEGY_SOURCE')}")

    # 4b) Enable pool_pre_ping so stale connections are recycled
    app.config.setdefault("SQLALCHEMY_ENGINE_OPTIONS", {})["pool_pre_ping"] = True

    # 5) Initialize all extensions *with retry* for transient DB faults
    @db_init_retry
    def init_extensions():
        with app.app_context():
            # ensure models are imported for Alembic
            from . import models  # noqa: F401

            cache.init_app(app)
            limiter.init_app(app)
            cors.init_app(app)
            db.init_app(app)
            migrate.init_app(app, db)
            executor.init_app(app)
            logger.debug("All extensions initialized")

    init_extensions()

    # 6) Register blueprints
    from .public_api import public_api as public_api_bp

    app.register_blueprint(public_api_bp, url_prefix="/api/v1/public")

    from .routes.strategy import bp as bp_strategy
    from .routes.arena import bp as bp_arena
    from .routes.data.stats import bp as bp_stats
    from .routes.admin import bp as bp_admin
    from .routes.user import bp as bp_user

    app.register_blueprint(bp_strategy, url_prefix="/strategy")
    app.register_blueprint(bp_arena, url_prefix="/arena")
    app.register_blueprint(bp_stats, url_prefix="/data/stats")
    app.register_blueprint(bp_admin, url_prefix="/admin")
    app.register_blueprint(bp_user, url_prefix="/user")

    # 7) Auth check on every request (except public API)
    @app.before_request
    def check_auth():
        if request.path.startswith("/api/v1/public/"):
            return
        if request.path.startswith("/arena/leaderboard"):
            return

        user_json = request.headers.get("X-User", "{}")
        user = json.loads(user_json or "{}")
        # logger.debug(f"User from header: {user}")
        if not user:
            logger.warning("Unauthorized request, no user found in header")
            return jsonify({"error": "Unauthorized"}), 401
        g.current_user = user

    # 🔍 Inspect every route that Flask thinks it has

    for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
        logging.debug(f"{rule.methods} -> {rule.rule}")

    return app


def run():
    # When running with `flask run` or `python -m rpsa_backend`, this
    # will get invoked, and thanks to pool_pre_ping + retry,
    # transient timeouts and disconnects will be retried.
    create_app().run(host="0.0.0.0", port=5000)
