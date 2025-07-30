
from typing import Literal
from pathlib import Path

TemplateName = Literal["fantastic-cv"]
SRC_REPO = Path(__file__).parent
TEMPLATES_FOLDER = Path(__file__).parent / "templates"

TEMPLATE_NAME_MAIN: dict[TemplateName, str] = {
    "fantastic-cv": "fantastic-cv-main.j2.typ",
}

RESUME_SCHEMA_NAME = "resume_schema.json"
CTX_SCHEMA_NAME = "ctx_schema.json"
