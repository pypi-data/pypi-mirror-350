from pathlib import Path
import toml

import yaml


from . import models


def dump_empty_json(path: Path | str) -> None:
    with open(path, "w") as f:
        f.write(models.Resume.get_empty().model_dump_json(indent=2, by_alias=True))


def dump_empty_yaml(path: Path | str) -> None:
    with open(path, "w") as f:
        py_content = models.Resume.get_empty().model_dump(by_alias=True)
        yaml.dump(py_content, f, indent=2, sort_keys=False)


def dump_empty_toml(path: Path | str) -> None:
    with open(path, "w") as f:
        py_content = models.Resume.get_empty().model_dump(by_alias=True)
        toml_content = toml.dumps(py_content)
        f.write(toml_content)
