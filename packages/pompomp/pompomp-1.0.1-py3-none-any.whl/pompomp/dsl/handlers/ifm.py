"""
Handler to resolve [if ...], [else], [end] DSL blocks.

Transforms DSL conditional expressions into Oh My Posh-compatible Go-template syntax.

Supports:
    - Comparison operators: ==, !=, <, <=, >, >= (or eq, ne, lt, le, gt, ge)
    - Logical operators: and, or, not
    - Contains operator: [if .Env.ENV contains 'PROD']
    - Nested expressions with proper function wrapping

Examples:
    [if .UserName == 'root'] → {{ if eq .UserName "root" }}
    [if .A > 0 and .B < 5] → {{ if and (gt .A 0) (lt .B 5) }}
    [else] → {{ else }}
    [end] → {{ end }}
"""
import re
from typing import Any

from pompomp.dsl.handlers import resolve_template_var

RE_IF_BLOCK = re.compile(r"\[if (.+?)]")
RE_ELSE_BLOCK = re.compile(r"\[else]", re.DOTALL)
RE_END_BLOCK = re.compile(r"\[end]")

OPERATORS = {
    "==": "eq",
    "eq": "eq",
    "!=": "ne",
    "<>": "ne",
    "ne": "ne",
    ">": "gt",
    "gt": "gt",
    ">=": "ge",
    "ge": "ge",
    "<": "lt",
    "lt": "lt",
    "<=": "le",
    "le": "le",
    "contains": "contains",
}

LOGIC = {"and", "or", "not"}

RE_OPERATOR_EXPR = re.compile(
    r"(?P<left>[^\s()]+)\s*(?P<op>\b(eq|ne|lt|le|gt|ge|contains)\b|==|!=|<>|>=|<=|>|<)\s*(?P<right>[^\s()]+)"
)
RE_LOGICAL_EXPR = re.compile(r"\(?(.+)\)?\s+(and|or)\s+\(?(.+)\)?")
RE_NOT_EXPR = re.compile(r"not\s+(?P<target>[^\s)]+)")


def _translate_condition(cond: str, trace: bool = False) -> str:
    """
    Translate a condition from DSL into valid Go template syntax.

    Args:
        cond: A condition string (inside a [if ...] block).
        trace: If True, output transformation steps.

    Returns:
        str: A Go-compatible condition string.
    """
    cond = cond.strip()

    # step 1 : replace comparisons first
    def replace_op(match):
        op = OPERATORS[match.group("op")]
        left = match.group("left")
        right = match.group("right")
        if op == "contains":
            return f"contains {right} {left}"
        return f"{op} {left} {right}"

    cond = RE_OPERATOR_EXPR.sub(replace_op, cond)
    cond = RE_NOT_EXPR.sub(lambda m: f"not {m.group('target')}", cond)
    cond = RE_LOGICAL_EXPR.sub(lambda m: f"{m.group(2)} ({m.group(1)}) ({m.group(3)})", cond)

    result = resolve_template_var(cond, trace=trace)
    if trace:
        print(f"[TRACE] [if] condition: {cond} => {result}")
    return result


def resolve_if(value: str, trace: bool = False, *_args) -> Any:
    """
    Resolve DSL conditional blocks into Go template blocks.

    Args:
        value: String containing one or more [if], [else], [end] tags.
        trace: If True, print trace output during condition resolution.
        *_args: Placeholder for signature compatibility.

    Returns:
        A string where all DSL condition blocks are transformed to Go template syntax.
    """
    value = RE_IF_BLOCK.sub(lambda m: "{{ if " + _translate_condition(m.group(1), trace=trace) + " }}", value)
    value = RE_ELSE_BLOCK.sub("{{ else }}", value)
    value = RE_END_BLOCK.sub("{{ end }}", value)
    return value
