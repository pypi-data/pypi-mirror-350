"""Helpers for manipulating data templates.

Includes functions to replace placeholders, normalize names, and generate slugs.
"""
import re

import unicodedata


def replace_placeholders(template: str, pattern_template=r"\[\s*%s\s*]", **kwargs) -> str:
    """
    Replace placeholders in a template string.

    Placeholders must be wrapped with square brackets, like [PLACEHOLDER].
    Each key in kwargs will replace its matching placeholder.

    Args:
        template: The template string containing placeholders.
        pattern_template: Regex schema to match placeholders (default: [PLACEHOLDER]).
        **kwargs: Mapping of placeholder names to their replacement values.

    Returns:
        A string with all placeholders replaced.
    """
    if "%s" not in pattern_template:
        raise ValueError("pattern_template must contain exactly one '%s' placeholder.")

    for key, value in kwargs.items():
        safe_value = str(value) if value != "" else '""'
        pattern = re.compile(pattern_template % re.escape(key))
        template = pattern.sub(safe_value, template)
    return template


def normalize_author_name(name: str) -> str:
    """
    Normalize the author's name with first part Capitalized and the rest UPPERCASE.

    Args:
        name: The original author name.

    Returns:
        A normalized author name.
    """
    parts = name.strip().split()
    if not parts:
        return ""
    first = parts[0].capitalize()
    rest = " ".join(p.upper() for p in parts[1:])
    return f"{first} {rest}".strip()


def slugify(value: str) -> str:
    """
    Convert a string into a URL/filename-safe slug using underscores.

    Args:
        value: The input string to slugify.

    Returns:
        A simplified, lowercase, underscore-separated string.
    """
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[\s\-]+", "_", value)
