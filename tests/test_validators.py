"""
tests.test_validators

Tests for the reusable validation functions.
"""

from unittest.mock import patch

import pytest

from assemblage import validators


def test_valid_entry_point():
    """Tests that a valid entry point passes without error."""
    # Using a real, existing module and function from the standard library
    assert validators.validate_entry_point("os.path:join") is True


def test_valid_entry_point_dot_notation():
    """Tests that a valid entry point with dot notation passes."""
    assert validators.validate_entry_point("os.path.join") is True


def test_invalid_module_raises_error():
    """Tests that an invalid module raises ImportError."""
    with pytest.raises(ImportError, match="Module 'non_existent_module' not found"):
        validators.validate_entry_point("non_existent_module:some_function")


def test_invalid_function_raises_error():
    """Tests that an invalid function raises AttributeError."""
    with pytest.raises(
        AttributeError, match="Function 'non_existent_function' not found"
    ):
        validators.validate_entry_point("os.path:non_existent_function")


def test_invalid_format_raises_error():
    """Tests that an invalid entry point format raises ValueError."""
    with pytest.raises(ValueError, match="Entry point must be in"):
        validators.validate_entry_point("ospathjoin")


def test_unimportable_module_raises_error():
    """Tests that a module that exists but has import errors is handled."""
    # This is harder to test directly without creating a broken file,
    # but we can simulate the find_spec raising an error.
    with patch(
        "importlib.util.find_spec", side_effect=ImportError("Simulated import error")
    ):
        with pytest.raises(
            ImportError, match="Module 'some.broken.module' could not be imported"
        ):
            validators.validate_entry_point("some.broken.module:function")
