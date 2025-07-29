from flask import Blueprint, request, current_app
from .. import db
from ..models import Strategy, User
from sqlalchemy import select
import os
import re
from ..utils import onboarding_required


bp = Blueprint("admin", __name__)


@bp.get("/strategies")
@onboarding_required
def get_strategies():
    strategies = db.session.execute(select(Strategy)).scalars().all()
    return [
        {
            "id": strategy.id,
            "name": strategy.name,
            "module_name": strategy.module_name,
            "user_name": strategy.user.name,
            "is_deleted": strategy.is_deleted,
        }
        for strategy in strategies
    ]


@bp.get("/deletedstrategies")
@onboarding_required
def get_deleted_strategies():
    strategies = (
        db.session.execute(select(Strategy).where(Strategy.is_deleted == True))
        .scalars()
        .all()
    )
    return [
        {
            "id": strategy.id,
            "name": strategy.name,
            "module_name": strategy.module_name,
            "author_id": strategy.user_id,
            "is_deleted": strategy.is_deleted,
        }
        for strategy in strategies
    ]


@bp.put("/strategies/delete/<strategy_id>")
@onboarding_required
def delete_strategy(strategy_id):

    strategy = db.session.execute(
        select(Strategy).where(Strategy.id == strategy_id, Strategy.is_deleted == False)
    ).scalar()

    if not strategy:
        return {"error": "Not found"}, 404

    strategy.is_deleted = True

    startegy_file = os.path.join(
        current_app.config.get("STRATEGY_FOLDER", "instance/strategies"),
        f"{strategy.module_name}.py",
    )

    if os.path.exists(startegy_file):
        new_name = os.path.join(
            current_app.config.get("STRATEGY_FOLDER", "instance/strategies"),
            f"DELETED_{strategy.module_name}.del",
        )
        os.rename(startegy_file, new_name)

    db.session.commit()

    return {"message": "OK"}


@bp.put("/strategies/undelete/<strategy_id>")
@onboarding_required
def undelete_strategy(strategy_id):
    # @TODO: Implement auth

    # return {"error": "Unauthorized"}, 401

    strategy = db.session.execute(
        select(Strategy).where(Strategy.id == strategy_id, Strategy.is_deleted == True)
    ).scalar()

    if not strategy:
        return {"error": "Not found or already active"}, 404

    # Set the strategy as not deleted
    strategy.is_deleted = False

    strategy_folder = current_app.config.get("STRATEGY_FOLDER", "instance/strategies")
    deleted_file = os.path.join(strategy_folder, f"DELETED_{strategy.module_name}.del")
    original_file = os.path.join(strategy_folder, f"{strategy.module_name}.py")

    # Rename the file back to its original name if it exists
    if os.path.exists(deleted_file):
        os.rename(deleted_file, original_file)

    # Check if the author of this strategy still exists and is active
    author = db.session.execute(
        select(User).where(User.id == strategy.user_id, User.is_deleted == False)
    ).scalar()

    if not author:
        # Check if the author exists but is marked as deleted
        author = db.session.execute(
            select(User).where(User.id == strategy.user_id, User.is_deleted == True)
        ).scalar()

        if author:
            # Restore the deleted author
            author.is_deleted = False
            db.session.commit()
        else:
            # The author does not exist at all; recreate the author
            author_name = (
                strategy.user_name
            )  # Assuming strategy has author_name attribute
            new_author = User(name=author_name, is_deleted=False)

            db.session.add(new_author)
            db.session.commit()

            # Update the strategy with the new author ID
            strategy.author_id = new_author.id
            db.session.commit()

    db.session.commit()

    return {"message": "Strategy restored successfully", "strategy": strategy.id}, 200


@bp.put("/strategies/modify/<int:strategy_id>")
@onboarding_required
def modify_strategy(strategy_id):
    data = request.json
    column = data.get("column")
    new_value = data.get("new_value")

    # Fetch the strategy to modify
    strategy = db.session.execute(
        select(Strategy).where(Strategy.id == strategy_id, Strategy.is_deleted == False)
    ).scalar()

    if not strategy:
        return {"error": "Strategy not found"}, 404

    # Handle modification of standard fields like 'name' and 'module_name'
    # Handle modification of standard fields like 'name' and 'module_name'

    folder = current_app.config.get("STRATEGY_FOLDER", "instance/strategies")
    strategy_file_path = os.path.join(folder, f"{strategy.module_name}.py")

    if column == "name":
        # Update the name in the strategy file
        if os.path.exists(strategy_file_path):
            with open(strategy_file_path, "r") as file:
                file_content = file.read()

            # Replace the name in the strategy class
            updated_content = re.sub(
                r'(name\s*=\s*")[^"]+(")', f'name = "{new_value}"', file_content
            )

            with open(strategy_file_path, "w") as file:
                file.write(updated_content)

        strategy.name = new_value

    elif column == "module_name":
        # Rename the strategy file if module_name is changed
        old_file = strategy_file_path
        new_file = os.path.join(folder, f"{new_value}.py")

        if os.path.exists(old_file):
            os.rename(old_file, new_file)

        strategy.module_name = new_value

    # Handle the author name modification case
    elif column == "author_name":
        existing_author = db.session.execute(
            select(User).where(User.name == new_value, User.is_deleted == False)
        ).scalar()

        if existing_author:
            # Update strategy's author_id to the existing author's id
            strategy.author_id = existing_author.id
        else:
            # Update the author's name using the author_id in the strategy
            author = db.session.execute(
                select(User).where(
                    User.id == strategy.author_id, User.is_deleted == False
                )
            ).scalar()

            if author:
                author.name = new_value

    elif column:
        # Update any other column dynamically
        setattr(strategy, column, new_value)

    # Commit the changes to the database
    db.session.commit()

    return {"message": "Strategy updated successfully", "strategy": strategy.id}, 200


@bp.get("/orphaned_authors")
@onboarding_required
def get_orphaned_authors():
    orphaned_authors = (
        db.session.execute(
            select(User)
            .outerjoin(Strategy, User.id == Strategy.author_id)
            .where(User.is_deleted == False)  # Consider only non-deleted authors
            .group_by(User.id)
            .having(
                db.func.count(Strategy.id).filter(Strategy.is_deleted == False) == 0
            )
        )
        .scalars()
        .all()
    )

    return [{"id": author.id, "name": author.name} for author in orphaned_authors], 200


@bp.delete("/orphaned_authors/<int:author_id>")
@onboarding_required
def delete_orphaned_author(author_id):
    author = db.session.execute(
        select(User).where(User.id == author_id, User.is_deleted == False)
    ).scalar()

    if not author:
        return {"error": "Author not found"}, 404

    author.is_deleted = True
    db.session.commit()

    return {"message": "Author deleted successfully"}, 200


@bp.get("/get_authors")
@onboarding_required
def get_authors():
    authors = db.session.execute(select(User)).scalars().all()
    return [
        {"id": author.id, "name": author.name, "is_deleted": author.is_deleted}
        for author in authors
    ]


@bp.get("/deletedauthors")
@onboarding_required
def get_deleted_authors():
    authors = (
        db.session.execute(select(User).where(User.is_deleted == True)).scalars().all()
    )
    return [
        {"id": author.id, "name": author.name, "is_deleted": author.is_deleted}
        for author in authors
    ]


@bp.put("/authors/delete/<int:author_id>")
@onboarding_required
def delete_author(author_id):
    author = db.session.execute(
        select(User).where(User.id == author_id, User.is_deleted == False)
    ).scalar()

    if not author:
        return {"error": "Author not found"}, 404

    author.is_deleted = True
    db.session.commit()

    return {"message": "Author deleted successfully"}, 200


@bp.put("/authors/undelete/<int:author_id>")
@onboarding_required
def undelete_author(author_id):
    author = db.session.execute(
        select(User).where(User.id == author_id, User.is_deleted == False)
    ).scalar()

    if not author:
        return {"error": "Author not found"}, 404

    author.is_deleted = False
    db.session.commit()

    return {"message": "Author undeleted successfully"}, 200


@bp.put("/authors/modify/<int:author_id>")
@onboarding_required
def save_author(author_id):
    data = request.json
    column = data.get("column")
    new_value = data.get("new_value")

    author = db.session.execute(
        select(User).where(User.id == author_id, User.is_deleted == False)
    ).scalar()

    if not author:
        return {"error": "Author not found"}, 404

    if column:
        # Update any other column dynamically
        setattr(author, column, new_value)

    db.session.commit()

    return {"message": "Author modified successfully"}, 200
