"""Loader for template metadata (meta.yml) used to describe available prompt templates.

This module provides:
- A Pydantic model `TemplateMetadata` to represent metadata structure.
- A Pydantic model `Contributor` to describe optional contributors.
- A loader function `load_template_metadata` to parse and validate meta.yml files.

The metadata typically includes:
- Template name (display name)
- Author name and optional email
- Optional contributors list
- Version (optional)
- Optional description

Example of a meta.yml file:

---
name: "Dracula Plus"
author: "John Doe"
email: "john@example.com"
version: "1.0.0"
description: "A Dracula-inspired vibrant dark theme."
contributors:
  - name: "Jane Smith"
    email: "jane@example.com"
---

Usage:
    from loaders.metadata_loader import load_template_metadata

    metadata = load_template_metadata("templates/default/meta.yml")
    print(metadata.name, metadata.version)
"""
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel

from pompomp.constants import YAML_ENCODING


class Authors(BaseModel):
    """
    Represents an individual contributor or author.

    Attributes:
        name: Full name of the contributor.
        email: Optional email address.
    """
    name: str
    email: Optional[str] = None


class TemplateMetadata(BaseModel):
    """
    Represents metadata for a template.

    Attributes:
        name: Display name of the template.
        version: Optional version string.
        description: Optional description of the template.
        created: Optional creation date or string.
        authors: Optional list of contributors (including main author).
        tags: Optional list of keywords associated with the template.
    """
    name: str
    version: Optional[str] = None
    description: Optional[str] = None
    created: Optional[str] = None
    authors: Optional[List[Authors]] = None
    tags: Optional[List[str]] = None


def load_template_metadata(path: str | Path) -> TemplateMetadata:
    """
    Load and validate template metadata from a YAML file.

    Args:
        path: Path to the metadata YAML file.

    Returns:
        A validated TemplateMetadata object.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {path}")

    with path.open("r", encoding=YAML_ENCODING) as f:
        data = yaml.safe_load(f)

    return TemplateMetadata(**data)
