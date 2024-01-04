import torch

from src.distance_utils import (
    compute_distances_with_all_the_palettes,
    get_ground_truth_ranks,
    get_most_similar_app_ids,
)
from src.image_utils import prepare_image
from src.url_utils import from_gift_to_egs_url


def get_subset_of_pre_computed_data(
    pre_computed_palettes: dict[str, torch.tensor],
    pre_computed_app_ids: list[str],
    test_app_ids: list[str],
):
    palettes_subset = {}
    app_ids_subset = []

    for color_palette, app_id in zip(
        pre_computed_palettes,
        pre_computed_app_ids,
        strict=False,
    ):
        if app_id in test_app_ids:
            palettes_subset[app_id] = color_palette
            app_ids_subset.append(app_id)

    return palettes_subset, app_ids_subset


def process_every_gift(
    egs_solutions: dict,
    pre_computed_palettes: dict[str, torch.tensor],
    pre_computed_app_ids: list[str],
    test_app_ids: list[str],
    params: dict,
    verbose: bool = False,
) -> list[int | None]:
    palettes_subset, app_ids_subset = get_subset_of_pre_computed_data(
        pre_computed_palettes,
        pre_computed_app_ids,
        test_app_ids,
    )

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

        distance_dict = compute_distances_with_all_the_palettes(
            reference_colors,
            palettes_subset,
            app_ids_subset,
            params,
            verbose=verbose,
        )

        most_similar_app_ids = get_most_similar_app_ids(distance_dict)

        ground_truth_ranks = get_ground_truth_ranks(
            gift["appids"],
            most_similar_app_ids,
        )
        gift_rank = min(ground_truth_ranks) if ground_truth_ranks else None

        gift_ranks.append(gift_rank)

    return gift_ranks
