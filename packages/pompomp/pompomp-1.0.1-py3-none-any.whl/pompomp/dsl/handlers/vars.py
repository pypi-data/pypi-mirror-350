"""
Handler to resolve [.XXX] blocks into OMP Go-template variables.

This module converts template variable blocks like `[.Shell]`, `[.UserName]` into
the corresponding Go-template syntax `{{ .Shell }}` or `{{ .UserName }}`.

Only matches blocks that:
- Start with a capital letter after the leading dot.
- Follow the naming convention of Oh My Posh variables.

Functions:
    - resolve_template_var(value: str, trace: bool = False, ...) -> str
"""
import re

from rich.markup import escape

# Matches [.XXX] with optional whitespace and dot-prefixed variables starting with a capital letter
TEMPLATE_VAR_PATTERN = re.compile(r"\[(\s*\.[A-Z][a-zA-Z0-9_.]*\s*)]")


def resolve_template_var(value: str, trace: bool = False, target_key: str | None = None, theme: str = "default") -> str:
    """
    Replace [.Var] blocks with {{ .Var }} for Go-template compatibility in OMP.

    Args:
        value (str): Input DSL string containing [.XXX] blocks.
        trace (bool): If True, prints trace logs for each transformation.
        target_key (str, optional): Unused. For DSL compatibility only.
        theme (str, optional): Active theme name. Unused here.

    Returns:
        str: Transformed string with escaped Go-template syntax.
    """
    matches = TEMPLATE_VAR_PATTERN.findall(value)
    transformed = value
    for match in matches:
        var = match.strip()
        replacement = f"{{{{ {var} }}}}"
        transformed = transformed.replace(f"[{match}]", escape(replacement))
        if trace:
            print(f"[TRACE] [{match}] => {replacement}")
    return transformed
