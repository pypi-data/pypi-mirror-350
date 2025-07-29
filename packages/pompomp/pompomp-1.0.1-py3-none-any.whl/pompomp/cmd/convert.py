"""
convert.py – CLI command to convert OMP themes and configuration files
between YAML, JSON, and TOML formats.

This command supports any file that can be interpreted as a dictionary
structure and aims to provide clean format translation.

Options:
  -i, --input TEXT      Path to the input file (.yml/.json/.toml)
  -o, --output TEXT     Path to the output file with desired extension

Examples:
  pompomp convert -i theme.yml -o theme.json
  pompomp convert --input config.json --output config.toml
"""
import typer

from pompomp.dsl.formats import read_file, write_file


def convert(
        input_file: str = typer.Option(
            ...,
            "--input", "-i",
            help="Path to the input file (.yml/.json/.toml)"),
        output_file: str = typer.Option(
            ...,
            "--output", "-o",
            help="Path to the output file with desired extension"),
):
    """
    Convert an OMP-compatible file from one format to another.

    Examples:
        pompomp convert -i theme.yml -o theme.json
        pompomp convert --input config.json --output config.toml

    Args:
        input_file (str): The path to the file to convert.
        output_file (str): The destination path, with the desired format extension.
    """
    data = read_file(input_file)
    write_file(data, output_file)
    typer.echo(f"✅ Converted {input_file} → {output_file}")
