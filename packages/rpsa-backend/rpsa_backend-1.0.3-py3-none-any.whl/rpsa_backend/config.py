import os
import logging


import os
import logging


class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or os.environ.get("FLASK_SQLALCHEMY_DATABASE_URI")
        or "sqlite:///rpsa.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_STRATEGY_RUNTIME = os.environ.get("MAX_STRATEGY_RUNTIME", "0.1").lower()

    # Strategy storage: either 'local' or 'blob'
    STRATEGY_SOURCE = os.environ.get("STRATEGY_SOURCE", "local").lower()
    # only used in local mode:
    STRATEGY_FOLDER = os.environ.get("STRATEGY_FOLDER", "instance/strategies")

    # only used in blob mode:
    BLOB_CONN_STRING = os.environ.get("BLOB_CONN_STRING")
    BLOB_CONTAINER = os.environ.get("BLOB_CONTAINER")
    # optional prefix in the container, e.g. "prod/"
    BLOB_PREFIX = os.environ.get("BLOB_PREFIX", "")

    # Logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    logger.debug(f"STRATEGY_SOURCE: {STRATEGY_SOURCE}")
    if STRATEGY_SOURCE == "local":
        logger.debug(f"STRATEGY_FOLDER: {STRATEGY_FOLDER}")
    else:
        logger.debug(f"BLOB_CONTAINER: {BLOB_CONTAINER}, BLOB_PREFIX: {BLOB_PREFIX}")

    # === ML MODEL storage settings ===
    # local vs. blob
    MODEL_SOURCE = os.environ.get("MODEL_SOURCE", "local").lower()
    MODEL_FOLDER = os.environ.get("MODEL_FOLDER", "instance/models")
    # blob uses same BLOB_CONN_STRING & BLOB_CONTAINER
    MODEL_BLOB_PREFIX = os.environ.get("MODEL_BLOB_PREFIX", "models/")

    logger.debug(f"MODEL_SOURCE={MODEL_SOURCE}")
    if MODEL_SOURCE == "local":
        logger.debug(f"MODEL_FOLDER={MODEL_FOLDER}")
    else:
        logger.debug(f"MODEL_BLOB_PREFIX={MODEL_BLOB_PREFIX}")
