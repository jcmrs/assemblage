"""
assemblage.validators

Provides reusable validation functions for the Assemblage framework.
"""

import importlib.util


def validate_entry_point(entry_point: str):
    """
    Validates if a string entry point (e.g., 'module.submodule:function') is valid.
    Raises ImportError, AttributeError, or ValueError if not valid.
    """
    if ":" not in entry_point and "." not in entry_point:
        raise ValueError(
            "Entry point must be in 'path.to.module:function' or "
            "'path.to.module.function' format."
        )

    # Split module path from function name
    if ":" in entry_point:
        module_path, function_name = entry_point.rsplit(":", 1)
    else:
        # Fallback for dot notation
        module_path, function_name = entry_point.rsplit(".", 1)

    # Check if the module can be found
    try:
        spec = importlib.util.find_spec(module_path)
    except (ImportError, ValueError):
        # Handles cases where the module path itself is invalid
        raise ImportError(f"Module '{module_path}' could not be imported.")

    if spec is None:
        raise ImportError(f"Module '{module_path}' not found.")

    # Import the module and check for the function
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Could not execute module '{module_path}': {e}")

    if not hasattr(module, function_name):
        raise AttributeError(
            f"Function '{function_name}' not found in module '{module_path}'."
        )

    # If we got here, the entry point is valid
    return True
