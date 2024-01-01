import json
from pathlib import Path


def load_json(fname: str) -> dict | list[str]:
    with Path(fname).open(encoding="utf8") as f:
        return json.load(f)


def save_json(data: dict | list, fname: str) -> None:
    with Path(fname).open("w", encoding="utf8") as f:
        json.dump(data, f)
