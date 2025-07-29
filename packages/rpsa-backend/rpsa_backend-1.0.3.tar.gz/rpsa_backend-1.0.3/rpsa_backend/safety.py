import builtins
import importlib.util
import os
import tempfile
import importlib.util
from flask import current_app
from azure.storage.blob import BlobServiceClient
from .arena import Strategy
import logging

# Capture the real import function
_real_import = builtins.__import__

# Build a sanitized builtins dict for user code execution
SAFE_BUILTINS = {k: v for k, v in builtins.__dict__.items()}
# Remove dangerous builtins
for fn in ["open", "eval", "exec", "exit", "quit", "input"]:
    SAFE_BUILTINS.pop(fn, None)

# Modules allowed in user scripts (roots)
SAFE_MODULES = {
    "random",
    "math",
    "abc",
    "typing",
    "collections",
    "datetime",
    "numpy",  # allow numpy and submodules
    "tensorflow",  # allow tensorflow and submodules
    "torch",  # allow preprocessing with torch
    "onnxruntime",
    "importlib.util",
    "rpsa_sdk",
    "rpsa_sdk.strategy",
    "rpsa_sdk.helpers",
}

# Override import in safe builtins to delegate to real import for whitelisted modules


def _whitelisted_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".")[0]
    if root in SAFE_MODULES:
        return _real_import(name, globals, locals, fromlist, level)
    raise ImportError(f"Module {name!r} not whitelisted for user scripts")


# Install our custom import into the safe builtins
SAFE_BUILTINS["__import__"] = _whitelisted_import

# Maximum allowed runtime for a strategy's test game
MAX_STRATEGY_RUNTIME = 0.1


def safe_import_strategy(name: str) -> Strategy:
    """
    Safely import a strategy module by name, from either a local folder
    or an Azure Blob Storage container, according to STRATEGY_SOURCE.
    """
    cfg = current_app.config
    source = cfg.get("STRATEGY_SOURCE", "local").lower()

    if source == "local":
        # load from disk
        folder = cfg["STRATEGY_FOLDER"]
        module_path = os.path.join(folder, f"{name}.py")
        if not os.path.isfile(module_path):
            raise ImportError(f"Strategy file not found: {module_path}")

    else:
        # load from blob: download into a temp file
        conn_str = cfg["BLOB_CONN_STRING"]
        container_name = cfg["BLOB_CONTAINER"]
        prefix_name = cfg["BLOB_PREFIX"]
        blob_name = f"{prefix_name}/{name}.py"

        blob_client = (
            BlobServiceClient.from_connection_string(conn_str)
            .get_container_client(container_name)
            .get_blob_client(blob_name)
        )

        if not blob_client.exists():
            raise ImportError(f"Strategy blob not found: {blob_name}")

        # download to a temp file
        tf = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
        try:
            data = blob_client.download_blob().readall()
            tf.write(data)
            tf.flush()
        finally:
            tf.close()
        module_path = tf.name

    # now import under safe builtins
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    module.__builtins__ = SAFE_BUILTINS
    spec.loader.exec_module(module)

    # clean up temp file if we downloaded from blob
    if source != "local":
        try:
            os.remove(module_path)
        except OSError:
            pass

    if not hasattr(module, "strategy"):
        raise ImportError(f"Module '{name}' does not define a top-level 'strategy'")

    # Ensure the strategy class defines a class-level 'name' variable
    strategy_cls = module.strategy
    if not isinstance(strategy_cls, type) or "name" not in getattr(
        strategy_cls, "__dict__", {}
    ):
        raise ImportError(
            f"Strategy class '{getattr(strategy_cls, '__name__', str(strategy_cls))}' must define a class variable 'name'"
        )

    return module.strategy


PYTHON_ERROR_HELPER = {
    # Common Errors with lists
    "list indices must be integers or slices, not str": [
        "You may have tried to access a list element using a string as an index.",
        "Ensure that you are using an integer to access list elements.",
    ],
    "list index out of range": [
        "You are trying to access an index in a list that is beyond the current size of the list.",
        "Check your list indices to make sure they are within the valid range.",
    ],
    "'list' object is not callable": [
        "You may have accidentally used parentheses () instead of brackets [] to access a list element.",
        "Ensure that you use [] to access elements from a list, not ().",
    ],
    # Errors related to variable names
    "name 'history' is not defined": [
        "The variable 'history' is used before it is defined.",
        "Make sure that 'history' is initialized before using it, typically as an empty list in the class constructor.",
    ],
    "name 'random' is not defined": [
        "The 'random' module is being used without being imported.",
        "Add 'import random' at the top of your script.",
    ],
    "name 'self' is not defined": [
        "You may have forgotten to use 'self.' when referring to an instance variable or method.",
        "Ensure that you use 'self.' before accessing instance variables or methods within a class.",
    ],
    # Errors related to methods and attributes
    "'NoneType' object has no attribute": [
        "You might be calling a method or accessing an attribute on a variable that is None.",
        "Check that the variable is properly initialized before calling methods or accessing attributes.",
    ],
    "object has no attribute": [
        "You are trying to access an attribute or method that doesn't exist on the object.",
        "Check for typos in the attribute or method name and ensure it is defined.",
    ],
    # Errors related to syntax and operations
    "unsupported operand type(s) for +: 'int' and 'str'": [
        "You are trying to add an integer to a string, which is not allowed.",
        "Convert the integer to a string using str() before concatenating.",
    ],
    "division by zero": [
        "You are trying to divide a number by zero, which is not allowed.",
        "Ensure that the divisor is not zero before performing the division.",
    ],
    "invalid syntax": [
        "There is a syntax error in your code, such as a missing colon, parenthesis, or indentation error.",
        "Check the highlighted line and surrounding code for syntax issues.",
    ],
    # Import Errors
    "ImportError: No module named": [
        "You may have tried to import a module that is not installed or is not allowed.",
        "Check the module name for typos and ensure it is in the list of allowed modules.",
    ],
    # Type Errors
    "TypeError: 'int' object is not callable": [
        "You may have used parentheses () on an integer, which is not allowed.",
        "Ensure that you are not trying to call an integer as if it were a function.",
    ],
    "TypeError: 'str' object is not callable": [
        "You may have used parentheses () on a string, which is not allowed.",
        "Ensure that you are not trying to call a string as if it were a function.",
    ],
    "TypeError: 'float' object is not callable": [
        "You may have used parentheses () on a float, which is not allowed.",
        "Ensure that you are not trying to call a float as if it were a function.",
    ],
    # Attribute Errors
    "AttributeError: 'list' object has_no_attribute": [
        "You may have tried to call a method that doesn't exist for lists.",
        "Ensure that you are using valid list methods like append(), pop(), etc.",
    ],
    # Index Errors
    "IndexError: tuple index out of range": [
        "You are trying to access an index in a tuple that doesn't exist.",
        "Check your tuple indices to ensure they are within the valid range.",
    ],
    # Value Errors
    "ValueError: invalid literal for int() with base 10": [
        "You may have tried to convert a non-numeric string to an integer.",
        "Ensure that the string you are converting to an integer contains only digits.",
    ],
    "Invalid move": [
        "Ensure that the play() method in your strategy returns one of the valid moves: 'rock', 'paper', or 'scissors'.",
        "Check for typos in the move names returned by the play() method.",
        "Make sure that the play() method logic is correctly selecting from the valid options.",
    ],
}
