import torch

from src.distance_utils import (
    compute_distances_with_all_the_palettes,
    get_ground_truth_rank,
)
from src.image_utils import prepare_image
from src.url_utils import from_gift_to_egs_url


def process_every_gift(
    egs_solutions: dict,
    pre_computed_palettes: dict[str, torch.tensor],
    test_app_ids: list[str],
    params: dict,
    verbose: bool = False,
) -> list[int | None]:
    ground_truth_ranks = []
    for gift_index in range(len(egs_solutions["gift"])):
        gift = egs_solutions["gift"][gift_index]
        path_or_url = from_gift_to_egs_url(egs_solutions, gift)
        print(f"{gift['index']}) {path_or_url}")

        reference_colors = prepare_image(
            path_or_url,
            params,
            verbose=verbose,
        )

        distance_dict = compute_distances_with_all_the_palettes(
            reference_colors,
            pre_computed_palettes,
            test_app_ids,
            params,
            verbose=verbose,
        )

        appid_index = 0
        ground_truth_app_id = gift["appids"][appid_index]

        ground_truth_rank, most_similar_app_ids = get_ground_truth_rank(
            distance_dict,
            ground_truth_app_id,
        )

        ground_truth_ranks.append(ground_truth_rank)

    return ground_truth_ranks
