from pathlib import Path

import torch

from src.constants import (
    APPID_FNAME,
    FILTERED_APP_IDS_FNAME,
    HSV_PALETTE_FNAME,
    PALETTE_FNAME,
    POPULAR_APPIDS_FNAME,
    SOLUTIONS_FNAME,
)
from src.json_utils import load_json


def get_app_ids(fname: str = APPID_FNAME) -> list[str]:
    return [str(app_id) for app_id in load_json(fname)]


def get_test_fnames(image_folder: str, file_ext: str = ".jpg", verbose=True):
    test_fnames = sorted(Path(image_folder).glob(f"*{file_ext}"))
    if verbose:
        print(f"#images = {len(test_fnames)}")
    return test_fnames


def get_filtered_app_ids(fname: str = FILTERED_APP_IDS_FNAME) -> dict | list[str]:
    return load_json(fname)


def get_pre_computed_palettes(fname: str = PALETTE_FNAME) -> torch.tensor:
    return torch.load(fname)


def get_pre_computed_palettes_hsv(fname: str = HSV_PALETTE_FNAME) -> torch.tensor:
    return get_pre_computed_palettes(fname)


def get_egs_solutions(fname: str = SOLUTIONS_FNAME) -> dict | list[str]:
    return load_json(fname)


def get_popular_appids(fname: str = POPULAR_APPIDS_FNAME) -> list[str]:
    return get_app_ids(fname)
