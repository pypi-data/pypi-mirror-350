"""
Custom exception classes used across the pompomp project.

These exceptions are used to raise meaningful errors during configuration
loading and template resolution, instead of relying on generic system exits.
"""
class PompompConfigError(Exception):
    """Raised when the pompomp.yml is invalid, missing, or unreadable."""
    ...


class TemplatesRootNotInitialized(Exception):
    """Raised when the user templates path is not set in the configuration."""
    ...


class TemplatesRootNotFound(Exception):
    """Raised when the user templates directory does not exist."""
    ...


class ScaffoldError(Exception):
    """Raised when the user templates directory is not found."""
    ...
