"""Icons Loader

This module provides a loader utility for YAML-based theme icons using the
generic ResourcesLoader[Icons].

Functions:
    - load_icons(theme: str, templates_path: Path | None = None) -> Icons
"""
from pathlib import Path

from pompomp.constants import DEFAULT_ICONS_FILENAME, DEFAULT_SHARED_DIRNAME
from pompomp.loaders.resources_loader import ResourcesLoader
from pompomp.models.icons import Icons

__all__ = ["load_icons"]


def _transformer(data: dict, theme: str) -> Icons:
    """
    Custom transformer to convert raw YAML data into an Icons object.

    Args:
        data: Parsed icon data from YAML.
        theme: Name of the theme being loaded.

    Returns:
        Icons: Instance with resolved UI and general icon mappings.
    """
    return Icons(
        name=theme,
        ui=data.get("ui", {}),
        icons=data.get("icons", {}),
    )


_icons_loader = ResourcesLoader[Icons](
    cls=Icons,
    filename=DEFAULT_ICONS_FILENAME,
    shared_dir=DEFAULT_SHARED_DIRNAME,
    transformer=_transformer,
)


def load_icons(theme: str, templates_path: Path | None = None) -> Icons:
    """
    Load the icons for the given theme, with support for fallback.

    Args:
        theme: Name of the theme to load.
        templates_path: Optional custom templates base directory.

    Returns:
        Icons: Fully merged icon configuration.
    """
    if templates_path:
        _icons_loader.templates_path = templates_path
    return _icons_loader.load(theme)
