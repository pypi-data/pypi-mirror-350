from pathlib import Path
from typing import Literal, overload

from jinja2 import Environment, FileSystemLoader
import json
import yaml
import toml
import typst

from . import consts
from . import models

__all__ = ["generate_typ", "generate"]

ENV = Environment(loader=FileSystemLoader(consts.TEMPLATES_FOLDER), trim_blocks=True)

OutputFormat = Literal["typ", "pdf", "str"]


def generate_typ(
    model: models.Resume,
    template_name: consts.TemplateName,
    output_path: Path | str,
    render_ctx: models.RenderCtx = models.RenderCtx(),
) -> None:
    _output_path = Path(output_path)
    template = ENV.get_template(consts.TEMPLATE_NAME_MAIN[template_name])
    with open(_output_path, "w", encoding="utf-8") as f:
        f.write(template.render({"resume": model, "ctx": render_ctx}))


@overload
def generate(
    src: models.Resume,
    output_path: Path | str,
    template_name: consts.TemplateName,
    render_ctx: models.RenderCtx = models.RenderCtx(),
) -> None: ...


@overload
def generate(
    src: str,
    output_path: Path | str,
    template_name: consts.TemplateName,
    render_ctx: models.RenderCtx = models.RenderCtx(),
) -> None: ...


@overload
def generate(
    src: Path,
    output_path: Path | str,
    template_name: consts.TemplateName,
    render_ctx: models.RenderCtx = models.RenderCtx(),
) -> None: ...


def generate(src, output_path, template_name, render_ctx=models.RenderCtx()) -> None:
    """Generate a CV from a JSON, YAML, or TOML string or file path.
    Args:
        src: The source JSON, YAML, or TOML string or file path.
        output_path: The output file path. Could be one of the following formats:
            - typ: Typst file
            - pdf: PDF file
            - svg: SVG file
            - png: PNG file
            - html: HTML file
        template_name: The name of the template to use.
        render_ctx: The render context to use.
    """
    path_maybe = Path(src)
    if not (set(str(src)) & set(["{", "["])) and path_maybe.exists():
        return generate(
            path_maybe.read_text(encoding="utf-8"), output_path, template_name, render_ctx
        )
    parsed_content = None
    try:
        parsed_content = json.loads(src)
    except Exception:
        pass

    if parsed_content is None:
        try:
            parsed_content = yaml.safe_load(src)
        except Exception:
            pass

    if parsed_content is None:
        try:
            parsed_content = toml.loads(src)
        except Exception:
            pass

    if parsed_content is None:
        raise ValueError("src must be a valid JSON, YAML, or TOML string or file path.")

    model = models.Resume.model_validate(parsed_content)

    custom_section_titles = [section.title for section in model.custom_sections]
    for section_name in render_ctx.section_order:
        if section_name in models.DEFAULT_SECTIONS:
            continue
        if section_name not in custom_section_titles:
            raise ValueError(
                f"Section '{section_name}' not found in the resume model. "
                + "Please check the section order."
            )

    generate_from_model(
        model=model,
        output_path=output_path,
        template_name=template_name,
        render_ctx=render_ctx,
    )


def generate_from_model(
    model: models.Resume,
    output_path: str | Path,
    template_name: consts.TemplateName,
    render_ctx,
) -> None:
    custom_section_titles = [section.title for section in model.custom_sections]
    for section_name in render_ctx.section_order:
        if section_name in models.DEFAULT_SECTIONS:
            continue
        if section_name not in custom_section_titles:
            raise ValueError(
                f"Section '{section_name}' not found in the resume model. "
                + "Please check the section order."
            )

    _output_path = Path(output_path)
    suffix = _output_path.name.split(".")[-1]
    _output_path.parent.mkdir(parents=True, exist_ok=True)
    if suffix == "typ":
        generate_typ(model, template_name, _output_path, render_ctx)
    elif suffix in ["pdf", "svg", "png", "html"]:
        temp_path = _output_path.with_suffix(".typ")
        generate_typ(model, template_name, temp_path, render_ctx)
        try:
            # File is already closed from the with block
            typst.compile(str(temp_path), str(output_path), format=suffix)  # type: ignore
        finally:
            temp_path.unlink()
    else:
        raise ValueError(
            "output_path must end with typ, pdf, svg, png, or html. "
            + f"Got: {_output_path.name}"
        )
