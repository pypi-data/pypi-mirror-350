"""This script generates test files for the Resume model for testing purposes.
Files that will be generated are json, yaml, and toml files.
"""

from pathlib import Path
import yaml
import toml


import cv_model

ROOT = Path(__file__).parent.parent
TEST_FOLDER = ROOT / "tests"
DATA_FILES_FOLDER = TEST_FOLDER / "data_files"


def generate_test_files():
    """Generate test files for the Resume model."""
    # Generate valid resume
    with open(DATA_FILES_FOLDER / "example_resume.json", "w", encoding="utf-8") as f:
        f.write(cv_model.models.get_default_resume().model_dump_json(by_alias=True, indent=2))
    print(f"json file generated at {DATA_FILES_FOLDER / 'example_resume.json'}")
    with open(DATA_FILES_FOLDER / "example_resume.yaml", "w", encoding="utf-8") as f:
        yaml.dump(
            cv_model.models.get_default_resume().model_dump(by_alias=True), f, allow_unicode=True
        )
    print(f"yaml file generated at {DATA_FILES_FOLDER / 'example_resume.yaml'}")
    with open(DATA_FILES_FOLDER / "example_resume.toml", "w", encoding="utf-8") as f:
        toml.dump(cv_model.models.get_default_resume().model_dump(by_alias=True), f)
    print(f"toml file generated at {DATA_FILES_FOLDER / 'example_resume.toml'}")

if __name__ == "__main__":
    generate_test_files()
