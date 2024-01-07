import torch

from src.distance_utils import (
    get_ground_truth_ranks,
    get_most_similar_app_ids,
)
from src.image_utils import prepare_image
from src.score_utils import compute_distance_between_palettes
from src.url_utils import from_gift_to_egs_url


def get_subset_of_pre_computed_data(
    pre_computed_palettes: torch.tensor,
    pre_computed_app_ids: list[str],
    test_app_ids: list[str],
) -> tuple[torch.tensor, list[str]]:
    indices_subet = []
    app_ids_subset = []

    for i, app_id in enumerate(pre_computed_app_ids):
        if app_id in test_app_ids:
            indices_subet.append(i)
            app_ids_subset.append(app_id)

    palettes_subset = pre_computed_palettes[indices_subet, :]

    return palettes_subset, app_ids_subset


def process_every_gift(
    egs_solutions: dict,
    pre_computed_palettes: torch.tensor,
    pre_computed_app_ids: list[str],
    test_app_ids: list[str],
    params: dict,
    verbose: bool = False,
) -> list[int | None]:
    # NB: we assume that the pre-computed palettes have
    # already been processed with to_linear_hsv() if needed.

    if test_app_ids:
        palettes_subset, app_ids_subset = get_subset_of_pre_computed_data(
            pre_computed_palettes,
            pre_computed_app_ids,
            test_app_ids,
        )
    else:
        palettes_subset = pre_computed_palettes
        app_ids_subset = pre_computed_app_ids

    gift_ranks = []
    for gift_index in range(len(egs_solutions["gift"])):
        gift = egs_solutions["gift"][gift_index]
        path_or_url = from_gift_to_egs_url(egs_solutions, gift)
        print(f"{gift['index']}) {path_or_url}")

        reference_colors = prepare_image(
            path_or_url,
            params,
            verbose=verbose,
        )

        distance = compute_distance_between_palettes(
            reference_colors,
            palettes_subset,
            params,
        )

        most_similar_app_ids = get_most_similar_app_ids(
            distance,
            app_ids_subset,
            params["topk"],
        )

        ground_truth_ranks = get_ground_truth_ranks(
            gift["appids"],
            most_similar_app_ids,
        )
        gift_rank = min(ground_truth_ranks) if ground_truth_ranks else None

        gift_ranks.append(gift_rank)

    return gift_ranks
