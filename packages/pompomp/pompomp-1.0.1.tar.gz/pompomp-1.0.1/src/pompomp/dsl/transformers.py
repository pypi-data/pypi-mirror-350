"""
DSL Transformers : Handles recursive parsing and transformation of DSL values.

This module provides functions to process and resolve custom DSL blocks like:
    - [inc:...], [inc_var:...]
    - [palette:...], [ui:...], [icons:...]
    - conditional blocks: [if ...], [else], [end]
    - variable substitution and template resolution

Each DSL directive is handled by its associated function defined in `KEY_HANDLERS`.
Recursive includes are supported, with stack tracking to prevent infinite loops.
Multiline DSL blocks are flattened for safe parsing.

Functions:
    - transform_value: Main entrypoint for resolving any DSL-compatible value.
    - transform_block: Applies DSL transformation to a full dictionary block.
    - resolve_dsl_string: Resolves all DSL blocks in a string.
    - preprocess_value: Preprocesses a string (template vars, conditionals, styles).
"""
import re
from typing import Any, Callable, Dict, Optional

import yaml

from pompomp.constants import (
    DEFAULT_LAYOUTS_DIRNAME,
    DEFAULT_THEME_DIRNAME,
    TEMPLATES_METADATA_FILENAME,
    TEMPLATES_ROOT,
    YAML_ENCODING,
)
from pompomp.dsl.handlers import (
    clean_golang_template,
    resolve_icons,
    resolve_include,
    resolve_palette,
    resolve_template_var,
    resolve_ui,
    resolve_styles,
)
from pompomp.dsl.handlers.ifm import resolve_if

# --- DSL mapping ---

KEY_HANDLERS: Dict[str, Callable[[str, bool, str | None, str], Any]] = {
    "inc": resolve_include,
    "inc_var": None,  # filled after defining resolve_include_with_vars
    "palette": resolve_palette,
    "ui": resolve_ui,
    "icons": resolve_icons,
}

DSL_PATTERN = re.compile(r"\[([a-z_]+:[^\[\]]+)]")

# --- Tracing ---

def trace_log(key: str, input_val: Any, output_val: Any) -> None:
    """Prints a trace log for a resolved DSL block."""
    print(f"[TRACE] key={key} | input={input_val} | result={output_val}")

# --- Pre-processing ---

def preprocess_value(value: str, trace: bool = False, variables: Optional[dict[str, str]] = None) -> str:
    """
    Applies preprocessing to a DSL string.

    Handles variable interpolation (${var}), template vars, conditions ([if]), and styles.
    """
    if variables:
        for key, val in variables.items():
            pattern = re.compile(r"\$\{\s*" + re.escape(key) + r"\s*}")
            value = pattern.sub(val, value)
    value = resolve_template_var(value, trace=trace)
    value = resolve_if(value, trace=trace)
    value = resolve_styles(value, trace=trace)
    return value


def _load_meta(theme: str) -> dict[str, str]:
    """Loads the metadata file for the given theme."""
    meta_path = TEMPLATES_ROOT / theme / DEFAULT_LAYOUTS_DIRNAME / TEMPLATES_METADATA_FILENAME
    if not meta_path.exists():
        raise FileNotFoundError(f"{TEMPLATES_METADATA_FILENAME} not found at expected location: {meta_path}")
    with open(meta_path, "r", encoding=YAML_ENCODING) as f:
        return yaml.safe_load(f)


def resolve_include_with_vars(path: str, trace: bool = False, _target_key: Optional[str] = None,
                              theme: str = DEFAULT_THEME_DIRNAME) -> str:
    """
    Resolves [inc_var:...] DSL block by interpolating metadata variables in the path.

    Returns a new [inc:...] block ready for resolution.
    """
    meta = _load_meta(theme)
    variables = {k: str(v) for k, v in meta.items()}
    interpolated = preprocess_value(path, trace=trace, variables=variables)
    return f"[inc:{interpolated}]"


KEY_HANDLERS["inc_var"] = resolve_include_with_vars

# --- Core Resolution Logic ---

def _minify_dsl_condition_block(value: str) -> str:
    """Strips line breaks and excess spaces from [if]... [end] condition blocks."""
    pattern = re.compile(r"\[if [^]]+].*?\[end]", re.DOTALL)

    def minify_block(match):
        return "".join(line.strip() for line in match.group(0).splitlines())

    return pattern.sub(minify_block, value)


def _flatten_multiline_blocks(value: str) -> str:
    """
    Converts multi-line DSL blocks to single-line form.

    Ensures consistent parsing by the DSL regex pattern.
    """
    pattern = re.compile(r"\[([a-z_]+):\s*((?:[^\[\]]|\n)*?)]", re.MULTILINE)

    def repl(match):
        prefix, inner = match.groups()
        compact = re.sub(r"\s+", "", inner)
        return f"[{prefix}:{compact}]"

    return pattern.sub(repl, _minify_dsl_condition_block(value))


def _resolve_single_block(match: str, trace: bool, key: str | None, theme: str = DEFAULT_THEME_DIRNAME,
                          stack: list[str] | None = None) -> Any:
    """
    Resolves a single DSL block using the registered handler.

    Handles recursion, tracing, and detection of cyclic includes.
    """
    if ":" not in match:
        return f"[{match}]"

    prefix, val = match.split(":", 1)
    stack = stack or []

    handler = KEY_HANDLERS.get(prefix)
    if handler:
        resolved = handler(val, trace, key, theme)

        if trace:
            trace_log(prefix, match, resolved)

        if prefix == "inc_var":
            return transform_value(resolved, trace=trace, theme=theme, stack=stack)

        if val in stack:
            raise RecursionError(f"Detected recursive include: {' → '.join(stack + [val])}")

        if isinstance(resolved, (dict, str)) and (not isinstance(resolved, str) or DSL_PATTERN.search(resolved)):
            return transform_value(resolved, trace=trace, theme=theme, stack=stack + [val])

        return resolved

    return f"[{match}]"


def resolve_dsl_string(value: str, trace: bool = False, key: str | None = None,
                       theme: str = DEFAULT_THEME_DIRNAME,
                       stack: list[str] | None = None) -> Any:
    """
    Resolves all DSL blocks in a string.

    Delegates block resolution to individual handlers via KEY_HANDLERS.
    """
    matches = DSL_PATTERN.findall(value)
    if len(matches) == 1 and value.strip() == f"[{matches[0]}]":
        return _resolve_single_block(matches[0], trace, key, theme, stack)

    transformed = value
    for match in matches:
        resolved = _resolve_single_block(match, trace, key, theme, stack)
        transformed = transformed.replace(f"[{match}]", str(resolved))

    return transformed


def transform_value(value: Any, key: str | None = None, trace: bool = False, theme: str = DEFAULT_THEME_DIRNAME,
                    stack: list[str] | None = None) -> Any:
    """
    Recursively transforms a DSL-compatible value (str, list, or dict).

    Applies preprocessing and resolves any embedded DSL blocks.
    """
    if isinstance(value, str):
        value = _flatten_multiline_blocks(value)
        value = preprocess_value(value, trace=trace)
        if DSL_PATTERN.search(value):
            return clean_golang_template(resolve_dsl_string(value, trace=trace, key=key, theme=theme, stack=stack))
        return clean_golang_template(value)

    if isinstance(value, list):
        expanded = []
        for v in value:
            resolved = transform_value(v, key=key, trace=trace, theme=theme, stack=stack)
            if isinstance(resolved, list):
                expanded.extend(resolved)
            else:
                expanded.append(resolved)
        return expanded

    if isinstance(value, dict):
        return {k: transform_value(v, key=k, trace=trace, theme=theme) for k, v in value.items()}

    return value


def transform_block(block: dict, trace: bool = False, theme: str = DEFAULT_THEME_DIRNAME) -> dict:
    """
    Recursively resolves all DSL values in a block.

    Repeats transformation until all includes are resolved.
    """
    while True:
        transformed = {
            k: transform_value(v, key=k, trace=trace, theme=theme, stack=[])
            for k, v in block.items()
        }

        yaml_text = yaml.dump(transformed)
        if "[inc:" not in yaml_text and "[inc_var:" not in yaml_text:
            break

        block = transformed

    return transformed