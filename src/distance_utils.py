import mediapy as media
import torch
from tqdm import tqdm

from src.color_utils import to_linear_hsv
from src.download_utils import get_image_url
from src.score_utils import compute_distance_between_palettes


def compute_distances_with_all_the_palettes(
    reference_colors: torch.tensor,
    pre_computed_palettes: dict[str, torch.tensor],
    test_app_ids: list[str],
    params: dict,
    verbose: bool = True,
) -> dict[str, float]:
    best_distance = None
    distance_dict = {}

    for i, app_id in tqdm(enumerate(test_app_ids)):
        dominant_colors = pre_computed_palettes[i]

        if params["use_hsv"]:
            test_colors = to_linear_hsv(dominant_colors, params["change_coordinates"])
        else:
            test_colors = torch.tensor(dominant_colors)

        distance = compute_distance_between_palettes(
            reference_colors,
            test_colors,
            params,
        )

        distance_dict[app_id] = distance

        if best_distance is None or distance < best_distance:
            best_distance = distance

            if verbose:
                url = get_image_url(app_id)
                print(
                    f"\tappID: {app_id} ; distance: {distance:.2f} ; url: {url}",
                )
                media.show_image(media.read_image(url))

    return distance_dict


def get_ground_truth_rank(
    distance_dict: dict[str, float],
    ground_truth_app_id: None | int = None,
) -> tuple[None | int, list[str]]:
    most_similar_app_ids = sorted(distance_dict, key=lambda x: distance_dict[x])

    if ground_truth_app_id:
        try:
            rank = most_similar_app_ids.index(str(ground_truth_app_id))
        except ValueError:
            rank = None
        print(
            f"Ground truth (appID = {ground_truth_app_id}) is ranked n°{rank}.",
        )
    else:
        rank = None

    return rank, most_similar_app_ids
