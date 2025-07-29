"""
Compute the target paths and fallback to use when scaffolding a new theme.

Args:
    theme_name: Name of the new theme to create.
    base_theme: Name of the theme to copy from.

Returns:
    A tuple with:
    - slug: normalized directory name
    - theme_dir: full path where the new theme will be created
    - base_template: path to the base theme to copy

Example:
    >>> resolve_scaffold_targets("my_new_theme", "default")
    ('my-new-theme', Path('/path/to/templates/my-new-theme'), Path('/path/to/templates/default'))
"""
from pathlib import Path

from pompomp.constants import TEMPLATES_ROOT
from pompomp.helpers.data import slugify


def resolve_scaffold_targets(
        theme_name: str,
        base_theme: str,
) -> tuple[str, Path, Path]:
    """
    Compute the target paths and fallback to use when scaffolding a new theme.

    Args:
        theme_name: Name of the new theme to create.
        base_theme: Name of the theme to copy from.

    Returns:
        A tuple with:
        - slug: normalized directory name
        - theme_dir: full path where the new theme will be created
        - base_template: path to the base theme to copy
    """
    slug = slugify(theme_name)
    theme_dir = TEMPLATES_ROOT / slug
    base_template = TEMPLATES_ROOT / base_theme

    return slug, theme_dir, base_template
