from flask import Blueprint, request, jsonify, abort
from .. import db
from ..models import User, ApiKey
import json
from ..utils import UserHeader, get_user
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
import logging
import secrets

from ..utils import onboarding_required

bp = Blueprint("user", __name__)


@bp.post("/onboard")
def create_user():
    user_header = json.loads(request.headers.get("X-User"))

    user = db.session.execute(
        select(User).where(User.oauth_email == user_header["email"])
    ).scalar()

    if user:
        return "User already onboarded", 400

    username_check = db.session.execute(
        select(User).where(User.username == request.json["username"])
    ).scalar()

    if username_check:
        return "Username taken", 400

    print("Full request:", request.json)
    print("birthDate:", request.json["birthDate"])
    print("agreedToDataHandling:", request.json["agreedToDataHandling"])

    born_datetime = None
    if "birthDate" in request.json:
        try:
            # Parse the provided ISO8601 timestamp (UTC)
            dt = datetime.strptime(request.json["birthDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
            # Convert from UTC to local timezone (e.g. UTC+1)
            local_tz = timezone(timedelta(hours=1))
            born_datetime = dt.replace(tzinfo=timezone.utc).astimezone(local_tz)
        except ValueError:
            return (
                "Invalid birthDate format. Expected ISO8601 format with milliseconds and Z.",
                400,
            )

    # Validate the python_knowledge value against the Enum choices if provided, otherwise default to ENTRY.
    python_knowledge = request.json["experience"]

    # registered_to_newsletter defaults to False if not provided.
    registered_to_newsletter = request.json.get("agreedToDataHandling", False)

    logging.info(
        "Creating new user: username=%s, name=%s, email=%s, oauth_email=%s, born_date=%s, python_knowledge=%s, registered_to_newsletter=%s",
        request.json["username"],
        request.json["name"],
        request.json["email"],
        user_header["email"],
        born_datetime,
        python_knowledge,
        registered_to_newsletter,
    )

    user = User(
        username=request.json["username"],
        name=request.json["name"],
        email=request.json["email"],
        oauth_email=user_header["email"],
        born_date=born_datetime,
        python_knowledge=python_knowledge,
        registered_to_newsletter=registered_to_newsletter,
    )

    db.session.add(user)
    db.session.commit()

    return "OK", 200


@bp.get("/check/username/<username>")
def check_username(username):
    user = db.session.execute(select(User).where(User.username.like(username))).scalar()

    return {"free": not user}


@bp.get("/check/email/<email>")
def check_email(email):
    user = db.session.execute(select(User).where(User.email.like(email))).scalar()

    return {"free": not user}


@bp.get("/exists")
def check_user():
    user = get_user(request.headers)

    return {"exists": bool(user)}


@bp.post("/api-key")
@onboarding_required
def create_api_key(user: User):
    """
    POST /user/api-key
    Generate and store a 32-character API key for the authenticated user.
    If the user already has an active key, returns that one.
    """
    # look for existing non-revoked key
    existing = (
        db.session.query(ApiKey).filter_by(user_id=user.id, revoked_at=None).first()
    )
    if existing:
        return jsonify({"api_key": existing.key}), 200

    # Generate a 32-hex string (16 random bytes)
    new_key = secrets.token_hex(16)
    record = ApiKey(key=new_key, user_id=user.id)
    db.session.add(record)
    db.session.commit()
    return jsonify({"api_key": new_key}), 201


@bp.get("/api-key")
@onboarding_required
def get_api_key(user: User):
    """
    GET /user/api-key
    Retrieve the authenticated user's active API key. 404 if none exists.
    """
    existing = (
        db.session.query(ApiKey).filter_by(user_id=user.id, revoked_at=None).first()
    )
    if not existing:
        abort(404, description="No API key found for this user.")
    return jsonify({"api_key": existing.key}), 200


@bp.delete("/api-key")
@onboarding_required
def revoke_api_key(user: User):
    """
    DELETE /user/api-key
    Revoke the current key and issue a new one.
    """
    current = (
        db.session.query(ApiKey).filter_by(user_id=user.id, revoked_at=None).first()
    )
    if current:
        current.revoked_at = datetime.utcnow()
    # create new key
    new_key = secrets.token_hex(16)
    record = ApiKey(key=new_key, user_id=user.id)
    db.session.add(record)
    db.session.commit()
    return jsonify({"api_key": new_key}), 200
