from typing import TypedDict
from typing_extensions import NotRequired
from werkzeug.datastructures import Headers
import json
from . import db
from sqlalchemy import select
from .models import User
from werkzeug.exceptions import Forbidden
from functools import wraps
from flask import request
import inspect

# see database correctly setting up


class UserHeader(TypedDict):
    name: NotRequired[str]
    email: str
    image: NotRequired[str]


def get_user(headers: Headers):
    user_header: UserHeader = json.loads(headers.get("X-User"))

    if user_header:
        user = db.session.execute(
            select(User).where(User.oauth_email == user_header["email"])
        ).scalar()

        return user


def onboarding_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_user(request.headers)

        if not user:
            raise Forbidden("User not onboarded")

        sig = inspect.signature(f)

        if "user" in sig.parameters:
            kwargs["user"] = user

        return f(*args, **kwargs)

    return decorated
