"""
formats.py – I/O utility functions to read and write OMP-compatible files
in YAML, JSON, or TOML format.

These helpers enable seamless format switching while preserving structure and Unicode support.
"""

import json

import toml
import yaml

from pompomp.core_constants import YAML_ENCODING

__all__ = ["read_file", "write_file"]


def read_file(path: str) -> dict:
    """
    Read a structured file and return its content as a Python dictionary.

    Supports YAML (.yml/.yaml), JSON (.json), and TOML (.toml) formats.

    Args:
        path (str): Path to the input file.

    Returns:
        dict: Parsed file content.

    Raises:
        ValueError: If the file extension is unsupported.
    """
    if path.endswith((".yml", ".yaml")):
        with open(path, "r", encoding=YAML_ENCODING) as f:
            return yaml.safe_load(f)
    elif path.endswith(".json"):
        with open(path, "r", encoding=YAML_ENCODING) as f:
            return json.load(f)
    elif path.endswith(".toml"):
        with open(path, "r", encoding=YAML_ENCODING) as f:
            return toml.load(f)
    else:
        raise ValueError(f"Unsupported file extension for {path}")


def write_file(data: dict, path: str) -> None:
    """
    Write a Python dictionary to a structured file.

    The output format is inferred from the file extension: .yml/.yaml, .json, or .toml.

    Args:
        data (dict): The dictionary to serialize.
        path (str): Path to the output file.

    Raises:
        ValueError: If the file extension is unsupported.
    """
    if path.endswith((".yml", ".yaml")):
        with open(path, "w", encoding=YAML_ENCODING) as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
    elif path.endswith(".json"):
        with open(path, "w", encoding=YAML_ENCODING) as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif path.endswith(".toml"):
        with open(path, "w", encoding=YAML_ENCODING) as f:
            toml.dump(data, f)
    else:
        raise ValueError(f"Unsupported file extension for {path}")
