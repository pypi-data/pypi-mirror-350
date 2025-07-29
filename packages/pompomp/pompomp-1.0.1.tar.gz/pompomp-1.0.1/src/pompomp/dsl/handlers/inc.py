"""
Handler for resolving [inc:...] DSL blocks.

Supports resolving YAML includes using dot-paths like 'shared.omp.colors'
from the theme templates directory.

Examples:
    [inc:shared.omp.colors] → loads 'shared/omp/colors.yml'

Supports:
    - Full file inclusion (returns entire dict or list)
    - Targeted key extraction (e.g., used inside 'properties' blocks)
    - Fallback to 'default' theme if not found in the current theme
"""

from pathlib import Path
from typing import Any, Optional

from pompomp.constants import TEMPLATES_ROOT, TEMPLATE_DEFAULT_ROOT, DEFAULT_THEME_DIRNAME
from pompomp.dsl.formats import read_file

TEMPLATES_ROOT = TEMPLATES_ROOT

def _find_include_file(path: str, theme: str) -> Path:
    """
    Resolve a dot-path (e.g., 'shared.omp.colors') into an absolute Path to the YAML file.

    Tries to find the file under the given theme first, then falls back to the default theme.

    Args:
        path (str): Dot-separated include path (e.g., 'shared.omp.colors').
        theme (str): The active theme name (used before falling back to 'default').

    Returns:
        Path: Path to the resolved YAML file.

    Raises:
        FileNotFoundError: If the file is not found in both the theme and default fallback.
    """
    parts = path.split(".")
    filename = parts[-1] + ".yml"
    relative_dir = Path(*parts[:-1])

    theme_path = TEMPLATES_ROOT / theme / relative_dir / filename
    fallback_path = TEMPLATE_DEFAULT_ROOT / relative_dir / filename

    if theme_path.exists():
        return theme_path
    if fallback_path.exists():
        return fallback_path

    raise FileNotFoundError(
        f"Include file not found in theme '{theme}' or fallback '{DEFAULT_THEME_DIRNAME}':\n"
        f"  tried: {theme_path}\n"
        f"  fallback: {fallback_path}"
    )

def _trace_include(trace: bool, path: str, full_path: Path, data: Any, target_key: Optional[str]) -> None:
    """
    Output a trace of the include resolution if tracing is enabled.

    Args:
        trace (bool): Whether to print trace output.
        path (str): The original DSL path (e.g., 'shared.omp.colors').
        full_path (Path): The actual resolved file path.
        data (Any): Parsed content of the file (dict or list).
        target_key (str, optional): Key being extracted (if any), or None for full include.
    """
    if not trace:
        return

    keys = list(data.keys()) if isinstance(data, dict) else "<list>" if isinstance(data, list) else "<non-dict>"
    location = f"key='{target_key}'" if target_key else "<raw>"
    print(f"[TRACE] Included {path} => {full_path} ({location}) => keys: {keys}")

def resolve_include(
        path: str,
        trace: bool = False,
        target_key: Optional[str] = None,
        theme: str = DEFAULT_THEME_DIRNAME,
) -> Any:
    """
    Resolve a [inc:...] block by loading a YAML include file and extracting its content.

    Resolves a dot-path like 'shared.omp.os_properties' to 'templates/<theme>/shared/omp/os_properties.yml',
    with a fallback to the 'default' theme if the file is not found.

    Extraction rules:
        • If target_key is provided (e.g. used inside 'properties'), only that key is returned.
        • If the file has only one top-level key, it is returned directly.
        • Otherwise, the full dict or list is returned as-is.

    Args:
        path (str): Dot-path to the file (e.g., 'shared.omp.colors').
        trace (bool): If True, prints include trace.
        target_key (str, optional): A specific key to extract from the file (used in [inc:...] inside blocks).
        theme (str): The theme to resolve from.

    Returns:
        Any: Extracted data (dict, list, or value), depending on file content and target_key.

    Raises:
        FileNotFoundError: If the file is not found in both theme and default.
        KeyError: If the target key is not found in the file.
        ValueError: If the file format is invalid or extraction is not possible.
    """
    full_path = _find_include_file(path, theme)
    data = read_file(str(full_path))

    if isinstance(data, list):
        target_key = None

    _trace_include(trace, path, full_path, data, target_key)

    if target_key:
        if not isinstance(data, dict):
            raise ValueError(f"Cannot extract key from non-dict include file: {full_path}")
        if target_key not in data:
            raise KeyError(f"Key '{target_key}' not found in included file: {full_path}")
        return data[target_key]

    if isinstance(data, dict) and len(data) == 1:
        return next(iter(data.values()))

    if isinstance(data, (dict, list)):
        return data

    raise ValueError(f"Unsupported include content in {full_path}: must be dict or list")
