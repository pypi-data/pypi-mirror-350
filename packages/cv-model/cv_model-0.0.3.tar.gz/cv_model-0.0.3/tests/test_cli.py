
from pathlib import Path
from typing import Literal

from typer.testing import CliRunner
import pytest

import cv_model
import cv_model.cli
import cv_model.consts

runner = CliRunner()


# Add md as a valid format when we implement it
@pytest.mark.parametrize(
    "fmt",
    ["json", "yaml", "toml"],
)
def test_cli_new_formats(tmp_path: Path, fmt: Literal["json", "yaml", "toml"]) -> None:
    """Test the CLI command for creating a new resume with different formats."""
    result = runner.invoke(cv_model.cli.app, ["new", "-o", str(tmp_path), "-f", fmt])
    assert result.exit_code == 0
    assert (tmp_path / f"{cv_model.cli.DEFAULT_NEW_RESUME_BASE_NAME}.{fmt}").exists()

def test_cli_create_ctx(tmp_path: Path) -> None:
    """Test the CLI command for creating a new context."""
    result = runner.invoke(cv_model.cli.app, ["create-ctx", "-o", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / f"{cv_model.cli.DEFAULT_NEW_CTX_BASE_NAME}.json").exists()

# add html as a output format when typst fixes the bug of rendering html...
@pytest.mark.parametrize("source_fmt", ["json", "yaml", "toml"])
@pytest.mark.parametrize("output_fmt", ["typ", "pdf", "svg", "png"])
@pytest.mark.parametrize("template_name",cv_model.consts.TEMPLATE_NAME_MAIN.keys())
@pytest.mark.parametrize("use_ctx", [True, False])
def test_cli_render(
    tmp_path: Path,
    source_fmt: Literal["json", "yaml", "toml"],
    output_fmt: Literal["typ", "pdf", "svg", "png"],
    template_name: cv_model.consts.TemplateName,
    use_ctx: bool,
) -> None:
    """Test the CLI command for rendering a resume with different formats."""
    sub_folder = tmp_path / "data_files"
    runner.invoke(cv_model.cli.app, ["new", "-o", str(sub_folder), "-f", source_fmt])
    result = runner.invoke(cv_model.cli.app, ["create-ctx", "-o", str(tmp_path)])
    base_args: list[str] = [
            "render",
            str(sub_folder / f"resume.{source_fmt}"),
            "-o",
            str(sub_folder / f"output.{output_fmt}"),
            "-t",
            template_name,
        ]
    if use_ctx:
        base_args += ["-c", str(tmp_path / f"{cv_model.cli.DEFAULT_NEW_CTX_BASE_NAME}.json")]
    result = runner.invoke(cv_model.cli.app, base_args)
    assert result.exit_code == 0
    assert (sub_folder / f"output.{output_fmt}").exists()
    assert (sub_folder / f"output.{output_fmt}").stat().st_size > 0, "Output file is empty"
