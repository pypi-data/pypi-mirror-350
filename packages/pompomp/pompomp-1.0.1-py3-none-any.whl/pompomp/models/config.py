"""
Models related to the global configuration of pompomp.

This module defines validation and structure enforcement for the `pompomp.yml`
file, including support for packaged and user template paths.
"""
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TemplatesRoot(BaseModel):
    """
    Configuration section for template paths.

    Attributes:
        packaged: Relative path inside the installed package (e.g., './templates').
        user: Absolute path to the user workspace for templates (or None if uninitialized).
    """

    packaged: str = Field(
        ...,
        description="Relative path to the packaged templates directory"
    )
    user: Optional[str] = Field(
        None,
        description="Absolute path to the user templates directory (or null)"
    )

    @classmethod
    @field_validator("packaged")
    def validate_packaged_path(cls, v: str) -> str:
        """Ensure the packaged path is relative (not absolute)."""
        if Path(v).is_absolute():
            raise ValueError("templates_root.packaged must be a relative path")
        return v

    @classmethod
    @field_validator("user")
    def validate_user_path(cls, v: Optional[str]) -> Optional[str]:
        """Ensure the user path is absolute if defined (or null)."""
        if v is not None and not Path(v).is_absolute():
            raise ValueError("templates_root.user must be an absolute path or null")
        return v


class PompompConfig(BaseModel):
    """
    Root configuration model for `pompomp.yml`.

    Attributes:
        templates_root: Contains paths to packaged and user templates directories.
    """

    templates_root: TemplatesRoot
