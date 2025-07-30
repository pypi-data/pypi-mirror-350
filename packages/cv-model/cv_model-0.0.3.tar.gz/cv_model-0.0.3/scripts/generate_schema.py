
import json
from pathlib import Path

import cv_model
import cv_model.consts

SCHEMA_ROOT = Path(__file__).parent.parent / "schemas"
RESUME_SCHEMA_PATH = SCHEMA_ROOT / cv_model.consts.RESUME_SCHEMA_NAME
CTX_SCHEMA_PATH = SCHEMA_ROOT / cv_model.consts.CTX_SCHEMA_NAME

def generate_resume_schema():
    """Generate the schema for the Resume model."""
    schema = cv_model.models.Resume.model_json_schema()
    with open(RESUME_SCHEMA_PATH, "w", encoding="utf-8") as f:
        f.write(json.dumps(schema, indent=2))

def generate_ctx_schema():
    """Generate the schema for the RenderCtx model."""
    schema = cv_model.models.RenderCtx.model_json_schema()
    with open(CTX_SCHEMA_PATH, "w", encoding="utf-8") as f:
        f.write(json.dumps(schema, indent=2))

if __name__ == "__main__":
    generate_resume_schema()
    print(f"Resume schema generated at {RESUME_SCHEMA_PATH}")
    generate_ctx_schema()
    print(f"Render context schema generated at {CTX_SCHEMA_PATH}")
