"""
The `rendercv.cli.commands` module contains all the command-line interface (CLI)
commands of RenderCV.
"""

import copy
import pathlib
from typing import Annotated, cast
from pathlib import Path

import typer
from rich import print
import json
import yaml
import toml
import typst

from . import __version__
from . import consts
from . import models
from . import render

DEFAULT_NEW_RESUME_BASE_NAME = "resume"
DEFAULT_NEW_CTX_BASE_NAME = "render_ctx"


def validate_path(path: str | None) -> Path:
    _path = Path(path).resolve() if path is not None else Path.cwd()
    if not _path.exists():
        _path.mkdir(parents=True, exist_ok=True)
    return _path


app = typer.Typer(
    rich_markup_mode="rich",
    add_completion=False,
    # to make `rendercv --version` work:
    invoke_without_command=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    # don't show local variables in unhandled exceptions:
    pretty_exceptions_show_locals=False,
)


@app.command(
    name="new",
    help=(
        "Generate a source input file to get started. Example: [yellow]cvmodel new"
        " source --f json[/yellow]. Details: [cyan]cvmodel new --help[/cyan]"
    ),
)
def cli_command_new(
    format_type: Annotated[
        str,  # Literal["json", "yaml", "toml", "md"],
        typer.Option(
            "-f",
            "--format",
            help=(
                "The format of the source file to create. "
                + "Available formats are: `json`, `yaml`, `toml`, or `md`."
            ),
        ),
    ] = "json",
    output_path: Annotated[
        str | None,
        typer.Option(
            "-o",
            "--output",
            help=(
                "The output path for the generated source file. "
                + "If not provided, the file will be created in the current directory."
            ),
        ),
    ] = None,
) -> None:
    empty_model_py = models.Resume.get_empty().model_dump(by_alias=True)
    output_file_path = (
        validate_path(output_path) / f"{DEFAULT_NEW_RESUME_BASE_NAME}.{format_type}"
    )
    if format_type == "json":
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(empty_model_py, f, indent=2)
    elif format_type == "yaml":
        with open(output_file_path, "w", encoding="utf-8") as f:
            yaml.dump(empty_model_py, f, indent=2)
    elif format_type == "toml":
        with open(output_file_path, "w", encoding="utf-8") as f:
            toml.dump(empty_model_py, f)
    elif format_type == "md":
        raise NotImplementedError
    else:
        raise ValueError(
            f"Invalid format type: {format_type}. "
            "Available formats are: `json`, `yaml`, `toml`, or `md`."
        )
    print(
        f"Source file created at: {output_file_path}. "
        f"Edit it and run [yellow]cvmodel render[/yellow] to generate your CV."
    )


@app.command(
    name="create-ctx",
    help=(
        "Create a json file with the default render context. Render context controls "
        "styling and rendering options of the output file. The generated file will "
        "be an option to command [yellow]cvmodel render[/yellow]."
    ),
)
def cli_command_create_render_ctx(
    output_path: Annotated[
        str | None,
        typer.Option(
            "-o",
            "--output",
            help=(
                "The output path for the generated render context file. "
                + "If not provided, the file will be created in the current directory."
            ),
        ),
    ] = None,
) -> None:
    """Create a json file with the default render context."""
    render_ctx = models.RenderCtx()
    render_ctx_dict = render_ctx.model_dump(by_alias=True)
    output_file_path = validate_path(output_path) / f"{DEFAULT_NEW_CTX_BASE_NAME}.json"

    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(render_ctx_dict, f, indent=2)
    print(f"Render context file created at: {output_file_path}")


TEMPLATE_KEY_STR = str(list(consts.TEMPLATE_NAME_MAIN.keys()))


@app.command(
    name="render",
    help="Render a CV from a source file. ",
)
def cli_command_render(
    source: Annotated[
        str,
        typer.Argument(
            ...,
            help=(
                "The source file to render. Could be an absolute or relative path to the cwd. "
                + "Available formats are: `json`, `yaml`, `toml`, or `md`."
            ),
        ),
    ],
    output_path: Annotated[
        str | None,
        typer.Option(
            "-o",
            "--output",
            help=(
                "The output path for the rendered file. Could be an absolute or relative path to the cwd. "
                + "Output file could be one of the following formats: `typ`, `pdf`, `svg`, `png`, or `html`. "
                + "If not provided, a default `output.pdf` file will be created in the current directory."
            ),
        ),
    ] = None,
    template_name: Annotated[
        str,
        typer.Option(
            "-t",
            "--template",
            help=(
                "The name of the template to use. "
                + f"Available templates are: {TEMPLATE_KEY_STR}."
            ),
        ),
    ] = "fantastic-cv",
    render_ctx: Annotated[
        str | None,
        typer.Option(
            "-c",
            "--context",
            help=(
                "The path to the render context file. The path should be absolute or relative to the cwd. "
                + "If not provided, the default render context will be used."
            ),
        ),
    ] = None,
) -> None:
    _input_path = Path(source).resolve()
    if not _input_path.exists():
        raise FileNotFoundError(f"Source file not found: {_input_path}")
    _output_path = Path(output_path).resolve() if output_path else Path.cwd() / "output.pdf"
    if template_name not in consts.TEMPLATE_NAME_MAIN:
        raise ValueError(
            f"Invalid template name: {template_name}. "
            f"Available templates are: {consts.TEMPLATE_NAME_MAIN.keys()}."
        )
    ctx_path = validate_path(render_ctx) if render_ctx else None
    if ctx_path is None or not ctx_path.exists():
        ctx = models.RenderCtx()
    else:
        with open(ctx_path, "r", encoding="utf-8") as f:
            ctx = models.RenderCtx.model_validate_json(f.read())

    render.generate(
        _input_path,
        _output_path,
        cast(consts.TemplateName, template_name),
        ctx,
    )
