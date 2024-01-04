import mediapy as media
import torch
from tqdm import tqdm

from src.color_utils import to_linear_hsv
from src.download_utils import get_image_url
from src.score_utils import compute_distance_between_palettes


def compute_distances_with_all_the_palettes(
    reference_colors: torch.tensor,
    pre_computed_palettes: torch.tensor,
    pre_computed_app_ids: list[str],
    params: dict,
    verbose: bool = True,
) -> dict[str, float]:
    best_distance = None
    distance_dict = {}

    for i, app_id in tqdm(enumerate(pre_computed_app_ids)):
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

        if verbose and (best_distance is None or distance < best_distance):
            best_distance = distance

            url = get_image_url(app_id)
            print(
                f"\tappID: {app_id} ; distance: {distance:.2f} ; url: {url}",
            )
            media.show_image(media.read_image(url))

    return distance_dict


def get_most_similar_app_ids(distance_dict: dict[str, float]) -> list[str]:
    return sorted(distance_dict, key=lambda x: distance_dict[x])


def get_ground_truth_rank(
    ground_truth_app_id: None | int,
    most_similar_app_ids: list[str],
) -> None | int:
    if ground_truth_app_id:
        try:
            rank = 1 + most_similar_app_ids.index(str(ground_truth_app_id))
            print(
                f"Ground truth (appID = {ground_truth_app_id}) is ranked n°{rank}.",
            )
        except ValueError:
            rank = None
            print(
                f"Ground truth (appID = {ground_truth_app_id}) is not in the ranking.",
            )
    else:
        rank = None

    return rank


def get_ground_truth_ranks(
    ground_truth_app_ids: list[None | int],
    most_similar_app_ids: list[str],
) -> list[int]:
    ground_truth_ranks = []
    for app_id in ground_truth_app_ids:
        rank = get_ground_truth_rank(app_id, most_similar_app_ids)

        if rank:
            ground_truth_ranks.append(rank)

    return ground_truth_ranks
