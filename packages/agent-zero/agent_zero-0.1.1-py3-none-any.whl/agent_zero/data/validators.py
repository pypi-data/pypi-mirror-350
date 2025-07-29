from typing import Any
import re


def is_valid_iso_language(lang_code: str) -> bool:
    """Check if lang_code is a two-letter, lowercase language code."""
    pattern = r"^[a-z]{2}$"
    return bool(re.match(pattern, lang_code))


def is_valid_voice_settings(param_1: Any, param_2: Any) -> bool:
    """
    Check if at least one voice setting parameter is provided.

    Args:
        param_1 (Any): The first voice setting parameter.
        param_2 (Any): The second voice setting parameter.

    Returns:
        bool: True if at least one parameter is provided, False otherwise.
    """
    return bool(param_1 or param_2)


def is_valid_end_call_time(seconds: int | None):

    if not seconds or seconds >= 60:
        return True

    return False
