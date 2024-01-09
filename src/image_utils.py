import mediapy as media
import torch

from src.color_utils import (
    change_hsv_coordinates_vectorized,
    extract_colors,
    to_color_space_sequential,
)
from src.constants import NUM_COLORS
from src.display_utils import show_colors


def requires_color_space_transformation(params):
    return params["color_space"] != "rgb"


def requires_change_of_coordinates(params):
    return params["color_space"].startswith("linear")


def prepare_image(path_or_url: str, params: dict, verbose: bool = True) -> torch.tensor:
    dominant_colors = extract_colors(path_or_url, num_colors=NUM_COLORS)
    reference_colors = torch.tensor(dominant_colors).unsqueeze(dim=0)

    if requires_color_space_transformation(params):
        reference_colors = to_color_space_sequential(
            reference_colors,
            output_color_space=params["color_space"],
        )
    if requires_change_of_coordinates(params):
        reference_colors = change_hsv_coordinates_vectorized(reference_colors)

    if verbose:
        media.show_image(media.read_image(path_or_url), width=616)
        show_colors(dominant_colors)

    return reference_colors
