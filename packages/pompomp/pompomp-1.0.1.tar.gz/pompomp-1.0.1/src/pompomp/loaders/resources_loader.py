"""
ResourcesLoader

This module provides a generic and reusable loader for structured YAML-based resources,
such as palettes, icons, or other theme components.

It supports:
- In-memory caching for faster retrieval.
- Fallback logic to the "default" theme if a resource is not found.
- Consistent resolution using the TEMPLATES_ROOT structure.

Classes:
    - ResourcesLoader[T]: Generic loader for typed resource files.

Functions:
    - merge_dicts(base, override): Recursive dict merge.
    - resolve_resource_data(theme, relative_path): Load and merge data from theme with fallback.

Example:
    >>> loader = ResourcesLoader(cls=Palette, filename="palette.yml")
    >>> palette = loader.load("delta")
"""
from pathlib import Path
from typing import Callable, Generic, TypeVar

import yaml

from pompomp.constants import (
    DEFAULT_PALETTE_FILENAME,
    DEFAULT_SHARED_DIRNAME,
    DEFAULT_THEME_DIRNAME,
    TEMPLATES_ROOT,
    YAML_ENCODING,
)

T = TypeVar("T")
CACHE = {}


def resolve_resource_data(theme: str, relative_path: str) -> dict:
    """
    Resolve resource data for a given theme with in-memory caching.

    The function attempts to load the specified resource from the given theme directory.
    If the resource is not found, it falls back to the 'default' theme. If the resource
    is already cached, it is directly returned from memory to optimize performance.

    Args:
        theme (str): Name of the theme to search within.
        relative_path (str): Relative path to the resource (e.g., 'shared/palette.yml').

    Returns:
        dict: Parsed YAML content as a dictionary if found, else an empty dictionary.

    Raises:
        FileNotFoundError: If the resource is not found in both the specified theme and the default theme.
    """
    cache_key = f"{theme}:{relative_path}"
    if cache_key in CACHE:
        return CACHE[cache_key]

    base_dir = TEMPLATES_ROOT / theme
    file_path = base_dir / relative_path
    data = {}

    if file_path.exists():
        with file_path.open("r", encoding=YAML_ENCODING) as f:
            data = yaml.safe_load(f) or {}
    else:
        default_path = TEMPLATES_ROOT / DEFAULT_THEME_DIRNAME / relative_path
        if default_path.exists():
            with default_path.open("r", encoding=YAML_ENCODING) as f:
                data = yaml.safe_load(f) or {}
        else:
            raise FileNotFoundError(f"Resource not found in 'default': {default_path}")

    CACHE[cache_key] = data
    return data


class ResourcesLoader(Generic[T]):
    """
    Generic loader for YAML-based resource files with fallback resolution.

    This class is designed to load YAML-based resources (like palette or icons) for a
    specific theme. If the requested resource is not found in the specified theme, it
    falls back to the "default" theme.

    Attributes:
        cls (type[T]): The class type to instantiate from the final merged data.
        filename (str): The YAML filename to load (e.g., "palette.yml").
        shared_dir (str): Subdirectory under the theme containing the file (default: "shared").
        templates_path (Path): Base directory path for all themes (default: TEMPLATES_ROOT).
        transformer (Callable[[dict, str], T]): Optional transformer to convert dict to an instance of T.
        encoding (str): Encoding used to read YAML files (default: "utf-8").
    """
    def __init__(
        self,
        cls: type[T],
            filename: str = DEFAULT_PALETTE_FILENAME,
            shared_dir: str = DEFAULT_SHARED_DIRNAME,
        templates_path: Path | None = None,
        transformer: Callable[[dict, str], T] | None = None,
        encoding: str = YAML_ENCODING,
    ):
        """
        Initialize the ResourcesLoader with theme-specific configurations.

        Args:
            cls (type[T]): The class type to instantiate from the final merged data.
            filename (str): The YAML filename to load (default is "palette.yml").
            shared_dir (str): Subdirectory where the file is located (default is "shared").
            templates_path (Path, optional): Base directory path for all themes (default is TEMPLATES_ROOT).
            transformer (Callable[[dict, str], T], optional): A custom transformer to convert the dictionary to the final object.
            encoding (str): File encoding to use when reading YAML files (default is "utf-8").
        """
        self.cls = cls
        self.filename = filename
        self.shared_dir = shared_dir
        self.templates_path = templates_path or TEMPLATES_ROOT
        self.transformer = transformer or self.default_transformer
        self.encoding = encoding

    def load(self, theme: str = DEFAULT_THEME_DIRNAME) -> T:
        """
        Load the specified resource from the theme, with fallback to 'default'.

        This method attempts to load the resource (e.g., palette, icons) from the
        specified theme. If not found, it will automatically fall back to the "default" theme.

        Args:
            theme (str): Theme name to start lookup from. Default is "default".

        Returns:
            T: An instance of the resource class populated with the parsed data.
        """
        relative_path = f"{self.shared_dir}/{self.filename}"
        data = resolve_resource_data(theme, relative_path)
        return self.transformer(data, theme)

    def default_transformer(self, data: dict, theme: str) -> T:
        """
        Default transformer for converting YAML data into the resource instance.

        If no custom transformer is provided, this method is used to instantiate
        the resource class with the parsed YAML data.

        Args:
            data (dict): Parsed YAML data from the resource file.
            theme (str): The theme name being processed.

        Returns:
            T: An instance of the specified resource class (`cls`) populated with the parsed data.
        """
        return self.cls(name=theme, **data)
