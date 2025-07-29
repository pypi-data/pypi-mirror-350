from flask import Blueprint
from .auth import api_key_required
from .extensions import limiter, cache
from .routes.arenas import bp as arenas_bp
from .routes.games import bp as games_bp
from .routes.strategies import bp as strategies_bp

public_api = Blueprint("public_api", __name__, url_prefix="/api/v1/public")
public_api.register_blueprint(arenas_bp)
public_api.register_blueprint(games_bp)
public_api.register_blueprint(strategies_bp)
