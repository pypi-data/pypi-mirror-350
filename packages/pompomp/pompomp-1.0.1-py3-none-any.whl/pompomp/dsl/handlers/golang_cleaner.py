"""
Final cleaner for Go Template strings.

This module removes unwanted spaces between logical Go Template blocks,
like between {{ end }} and {{ if ... }} to avoid YAML-induced artifacts.

Example:
    '{{ end }} {{ if .X }}' → '{{ end }}{{ if .X }}'
"""
import re


def clean_golang_template(value: str) -> str:
    """
    Clean unwanted spaces between Go Template blocks.

    Args:
        value: The string to clean (must be a string).

    Returns:
        A cleaned string, or the original value if not a string.
    """
    if not isinstance(value, str):
        return value  # Safety: only clean strings
    if not value:
        return value
    return re.sub(r"(\{\{\s*end\s*}})\s+(\{\{\s*(if|else|elsif) )", r"\1\2", value)
