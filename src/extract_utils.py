import torch
from tqdm import tqdm

from src.color_utils import extract_colors
from src.constants import NUM_COLORS, PALETTE_FNAME


def extract_from_scratch(test_fnames: list[str]) -> dict[str, torch.tensor]:
    # This extraction process takes ~ 20 minutes.

    pre_computed_palettes = torch.zeros(
        len(test_fnames),
        NUM_COLORS,
        len("RGB"),
        dtype=int,
    )

    for i, fname in tqdm(enumerate(test_fnames)):
        if torch.all(pre_computed_palettes[i] == 0):
            dominant_colors = extract_colors(fname, num_colors=NUM_COLORS)
            pre_computed_palettes[i] = torch.tensor(dominant_colors)

    torch.save(pre_computed_palettes, PALETTE_FNAME)

    return pre_computed_palettes
