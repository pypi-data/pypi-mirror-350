from ruamel.yaml import YAML

from pathlib import Path
from typing import NamedTuple, Dict


class Config(NamedTuple):
    locale: str = "cs"

    extension_to_runtime: Dict[str, str] = {
        "cs": "mono",
        "c": "c-gcc-linux",
        "pas": "freepascal-linux",
        "java": "java",
        "cpp": "cxx-gcc-linux",
        "py": "python3"
    }

    judges: Dict[str, str] = {
        "bin/codex_judge": "recodex-judge-normal",
        "bin/codex_shufflejudge": "recodex-judge-shuffle",
        "diff": "diff"
    }

    @classmethod
    def load(cls, config_path: Path):
        if not config_path.exists():
            return cls()
        yaml = YAML(typ="safe")
        config = yaml.load(config_path.open("r"))
        return cls(**config)
