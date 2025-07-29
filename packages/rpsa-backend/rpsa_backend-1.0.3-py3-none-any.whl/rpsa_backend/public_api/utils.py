# File: rpsa_backend/public_api/utils.py

"""
Utility helpers shared by the public-API blueprint.

* `paginate_query` – SQLAlchemy LIMIT/OFFSET pagination with Marshmallow serialization.
* `get_accessible_arena_or_404` – Centralises the “regular or mine” access rule for arenas.
"""

from math import ceil
from flask import request, jsonify, abort
from sqlalchemy import inspect, or_, func, select

from ..models import Arena as ArenaModel
from .. import db


def paginate_query(query, schema, default_per_page: int = 20):
    """
    Paginate a SQLAlchemy `query`, serialize through the given Marshmallow
    *schema class*, and return JSON with `data` and `pagination`.
    Works around SQL Server by counting over a subquery.
    """
    # --- parse page & per_page safely ---
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", default_per_page)), 1), 100)
    except ValueError:
        page, per_page = 1, default_per_page

    # --- count total via subquery to avoid OFFSET/LIMIT in COUNT ---
    subq = query.subquery()
    total = db.session.query(func.count()).select_from(subq).scalar() or 0

    # --- ensure deterministic ORDER BY before OFFSET/LIMIT ---
    if not getattr(query, "_order_by_clauses", None):
        desc = query.column_descriptions
        if not desc or not desc[0].get("entity"):
            raise RuntimeError(
                "Cannot infer default ORDER BY; please apply .order_by() to the query."
            )
        pk_col = inspect(desc[0]["entity"]).primary_key[0]
        query = query.order_by(pk_col)

    # --- fetch only this page ---
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    pages = ceil(total / per_page) if total else 1

    return jsonify(
        {
            "data": schema(many=True).dump(items),
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": pages,
            },
        }
    )


def get_accessible_arena_or_404(arena_id: int, user):
    """
    Retrieve the Arena row if and only if:
      - it is regular (is_regular == True), OR
      - it is owned by the given user.

    Otherwise abort with a 404 (hiding forbidden vs. missing).
    """
    arena = (
        db.session.query(ArenaModel)
        .filter(
            ArenaModel.id == arena_id,
            ArenaModel.is_deleted == False,
            or_(
                ArenaModel.is_regular == True,
                ArenaModel.user_id == user.id,
            ),
        )
        .first()
    )
    if not arena:
        abort(404, description="Arena not found.")
    return arena
