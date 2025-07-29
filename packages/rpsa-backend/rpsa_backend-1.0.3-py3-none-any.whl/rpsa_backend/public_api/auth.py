# auth.py
from functools import wraps
from flask import request, abort, current_app, g
from ..models import ApiKey
from .. import db


def api_key_required(f):
    """
    Protect endpoint with per-user API key stored in api_keys table.
    Expects `X-API-KEY` header matching a non-revoked ApiKey.key in DB.
    Sets `g.current_user` to the associated User.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if not key:
            abort(401, description="Missing API key.")
        # Look up ApiKey record that is not revoked
        api_key = (
            db.session.query(ApiKey)
            .filter(ApiKey.key == key, ApiKey.revoked_at.is_(None))
            .first()
        )
        if not api_key:
            abort(401, description="Invalid or revoked API key.")
        # attach current user to global
        g.current_user = api_key.user
        return f(*args, **kwargs)

    return decorated
