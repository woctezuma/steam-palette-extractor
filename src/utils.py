from pathlib import Path

import torch

from src.constants import (
    APPID_FNAME,
    FILTERED_APP_IDS_FNAME,
    PALETTE_FNAME,
    POPULAR_APPIDS_FNAME,
    SOLUTIONS_FNAME,
)
from src.json_utils import load_json


def get_app_ids(fname=APPID_FNAME):
    return [str(app_id) for app_id in load_json(fname)]


def get_test_fnames(image_folder, file_ext=".jpg"):
    return sorted(Path(image_folder).glob(f"*{file_ext}"))


def get_filtered_app_ids(fname=FILTERED_APP_IDS_FNAME):
    return load_json(fname)


def get_pre_computed_palettes():
    return torch.load(PALETTE_FNAME)


def get_egs_solutions(fname=SOLUTIONS_FNAME):
    return load_json(fname)


def get_popular_appids():
    return get_app_ids(POPULAR_APPIDS_FNAME)
