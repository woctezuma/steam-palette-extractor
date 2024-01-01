import json
from pathlib import Path


def load_json(fname):
    with Path(fname).open(encoding="utf8") as f:
        return json.load(f)


def save_json(data, fname):
    with Path(fname).open("w", encoding="utf8") as f:
        json.dump(data, f)
