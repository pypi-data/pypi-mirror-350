"""
CLI command to generate an OMP-compatible theme from a DSL file.

Options:
  -i, --input             Path to the DSL input file (.yml/.json/.toml)
  -o, --output            Optional path to save the generated output
  -dr, --dry-run               Show the result in the terminal instead of writing to a file
  -hx, --highlight-hex         Render hex color values with visual feedback

  --trace                      Show debug trace output during DSL transformation
  -t, --theme TEXT             Theme name used for resolving includes (default: "default")

  -p, --preview                Launch oh-my-posh preview of the theme
  -s, --shell [bash|zsh|pwsh]  Required when --preview is enabled
"""
from typing import Optional

import typer
import yaml

# noinspection PyShadowingBuiltins
from pompomp.cmd.console import (
    rprint as print,
    console,
    Panel,
    Syntax,
    Text,
)
from pompomp.constants import (
    TEMPLATE_DEFAULT_MAIN_LAYOUT,
    DEFAULT_THEME_DIRNAME,
    DEFAULT_MAIN_THEME_LAYOUT_FILENAME,
    YAML_ENCODING,
    TEMPLATE_PREVIEW_TEMP_PATH
)
from pompomp.dsl.formats import read_file, write_file
from pompomp.dsl.transformers import transform_block
from pompomp.helpers.colors import highlight_hex_colors

SHELL_INIT_COMMANDS = {
    "bash": 'eval "$(oh-my-posh init bash --config {path})"',
    "zsh": 'eval "$(oh-my-posh init zsh --config {path})"',
    "pwsh": 'oh-my-posh init pwsh --config "{path}" | Invoke-Expression',
}


def _validate_preview_args(preview: bool, shell: Optional[str]) -> Optional[str]:
    if preview and not shell:
        print("[bold red]❌ --preview requires --shell to be set.[/bold red]")
        raise typer.Exit(code=1)
    if shell and shell.lower() not in SHELL_INIT_COMMANDS:
        print(f"[bold red]❌ Unsupported shell:[/] '{shell}'. Supported: {', '.join(SHELL_INIT_COMMANDS)}")
        raise typer.Exit(code=1)
    return shell.lower() if shell else None


def _handle_dry_run_output(transformed: dict, highlight_hex: bool) -> str:
    yaml_text = yaml.dump(transformed, sort_keys=False, allow_unicode=True)
    if highlight_hex:
        lines = highlight_hex_colors(yaml_text, contrast=151)
        console.print(Panel(Text("\n").join(lines), title="[bold green]Dry Run Output (Transformed DSL)", expand=True))
    else:
        syntax = Syntax(yaml_text, "yaml", theme="monokai", line_numbers=False)
        print(Panel(syntax, title="[bold green]Dry Run Output (Transformed DSL)", expand=True))
    return yaml_text


def _print_preview_instructions(shell: str, path: str):
    init_command = SHELL_INIT_COMMANDS[shell].format(path=path)
    print("\n[bold cyan]✨ Preview command:[/bold cyan]")
    print(f"[dim]{init_command}[/dim]")
    print("\n[bold yellow]⚠️ This command is not auto-executed. Copy/paste it to preview your prompt.")
    print(
        "[bold yellow]ℹ️ To reset: restart your shell or source your profile (e.g. . ~/.zshrc or . $Profile)[/bold yellow]")


def generate(
        input_file: str = typer.Option(
            DEFAULT_MAIN_THEME_LAYOUT_FILENAME, "--input", "-i",
            help="Path to the DSL input file (.yml/.json/.toml)"
        ),
        output_file: Optional[str] = typer.Option(
            None, "--output", "-o",
            help="Optional path to save the output file"
        ),
        dry_run: bool = typer.Option(
            False, "--dry-run", "-dr",
            help="If set, prints output instead of writing it"
        ),
        trace: bool = typer.Option(
            False, "--trace",
            help="Enable debug traces for transformation"
        ),
        theme: str = typer.Option(
            DEFAULT_THEME_DIRNAME, "--theme", "-t",
            help="Theme name to use for includes"
        ),
        preview: bool = typer.Option(
            False, "--preview", "-p",
            help="Load the theme into the current shell using oh-my-posh"
        ),
        shell: Optional[str] = typer.Option(
            None, "--shell", "-s",
            help="Shell to use for preview (e.g., zsh, bash, pwsh)",
            case_sensitive=False
        ),
        highlight_hex: bool = typer.Option(
            False, "--highlight-hex", "-hx",
            help="Highlight HEX colors visually in the dry-run output"
        )
):
    raw_data = read_file(
        input_file if input_file != DEFAULT_MAIN_THEME_LAYOUT_FILENAME
        else str(TEMPLATE_DEFAULT_MAIN_LAYOUT)
    )
    transformed = transform_block(raw_data, trace=trace, theme=theme)

    resolved_shell = _validate_preview_args(preview, shell)
    preview_path = None

    if dry_run:
        yaml_text = _handle_dry_run_output(transformed, highlight_hex)
        if preview:
            TEMPLATE_PREVIEW_TEMP_PATH.write_text(yaml_text, encoding=YAML_ENCODING)
            preview_path = str(TEMPLATE_PREVIEW_TEMP_PATH)
    else:
        if not output_file:
            print("[bold red]❌ --output is required unless --dry-run is used.[/bold red]")
            raise typer.Exit(code=1)
        write_file(transformed, output_file)
        print(f"[bold green]✅ Output written to:[/bold green] {output_file}")
        if preview:
            preview_path = output_file

    if preview and preview_path:
        _print_preview_instructions(resolved_shell, preview_path)
