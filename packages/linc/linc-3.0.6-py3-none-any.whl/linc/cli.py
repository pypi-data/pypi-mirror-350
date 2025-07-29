from pathlib import Path

import typer
from importlib import metadata

app = typer.Typer(
    name="linc CLI",
    help="Converts raw lidar files (Licel format) to NC with a configuration file",
)


@app.command(no_args_is_help=True)
def convert(
    source_path: list[Path] = typer.Argument(..., dir_okay=False, readable=True),
    output_path: Path = typer.Option(..., "--output", "-o", file_okay=True),
    config_file: Path = typer.Option(
        None,
        "--config",
        "-c",
    ),
    legacy: bool = typer.Option(False, "--legacy", "-l"),
):
    ...
    # (source_path, output_file=output_path, config_file=config_file)


def version_callback(value: bool):
    if value:
        version = metadata.version("linc")
        typer.echo(f"linc-cli, version {version}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the Manage FastAPI version information.",
    ),
): ...
