import mediapy as media
import torch

from src.color_utils import extract_colors, to_linear_hsv
from src.constants import NUM_COLORS
from src.display_utils import show_colors


def prepare_image(path_or_url, use_hsv, change_coordinates, verbose=True):
    dominant_colors = extract_colors(path_or_url, num_colors=NUM_COLORS)
    if use_hsv:
        reference_colors = to_linear_hsv(dominant_colors, change_coordinates)
    else:
        reference_colors = torch.tensor(dominant_colors)

    if verbose:
        media.show_image(media.read_image(path_or_url), width=616)
        show_colors(dominant_colors)

    return reference_colors
