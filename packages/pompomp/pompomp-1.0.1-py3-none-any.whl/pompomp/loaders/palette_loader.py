"""
Palette Loader

This module provides a loader utility for YAML-based theme palettes,
using the generic ResourcesLoader[Palette] with a custom transformer.

Functions:
    - load_palette(theme, templates_path): Loads a palette with fallback logic.
"""
from pathlib import Path

from pompomp.constants import DEFAULT_PALETTE_FILENAME, DEFAULT_SHARED_DIRNAME
from pompomp.loaders.resources_loader import ResourcesLoader
from pompomp.models.palette import Palette

__all__ = ["load_palette"]


def _transformer(data: dict, theme: str) -> Palette:
    """
    Custom transformer to convert a raw dict into a Palette instance.

    Args:
        data: Parsed YAML dictionary containing meta, colors, and roles.
        theme: Name of the theme being loaded.

    Returns:
        A Palette object.
    """
    return Palette(
        name=theme,
        meta=data.get("meta", {}),
        colors=data.get("colors", {}),
        roles=data.get("roles", {}),
    )


_palette_loader = ResourcesLoader[Palette](
    cls=Palette,
    filename=DEFAULT_PALETTE_FILENAME,
    shared_dir=DEFAULT_SHARED_DIRNAME,
    transformer=_transformer,
)


def load_palette(theme: str, templates_path: Path | None = None) -> Palette:
    """
    Load the palette for the given theme, with support for fallback.

    Args:
        theme: Name of the theme to load.
        templates_path: Optional custom templates base directory.

    Returns:
        Fully merged Palette object.
    """
    if templates_path:
        _palette_loader.templates_path = templates_path
    return _palette_loader.load(theme)
