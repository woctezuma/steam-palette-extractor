from pathlib import Path

from src.constants import FILTERED_APP_IDS_FNAME, FILTERED_INDICES_FNAME
from src.json_utils import save_json


def prepare_filtered_files(app_ids, test_fnames):
    filtered_indices = []
    filtered_app_ids = []

    for fname in test_fnames:
        index = int(Path(fname).stem)

        filtered_indices.append(index)
        filtered_app_ids.append(app_ids[index])

    save_json(filtered_indices, FILTERED_INDICES_FNAME)
    save_json(filtered_app_ids, FILTERED_APP_IDS_FNAME)
