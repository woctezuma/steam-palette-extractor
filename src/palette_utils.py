import torch

from src.score_utils import to_score
from src.weight_utils import adjust_pairwise_distances, to_weights_target


def compute_min_of_weighted_color_distances(pairwise_distances, params, dim):
    if params.get("apply_target_in_color_distance"):
        num_elements = pairwise_distances.size()[dim]
        indices_target = torch.tensor(range(num_elements))

        target_weights = to_weights_target(
            indices_target,
            params,
            num_elements,
        )

        num_dimensions = len(pairwise_distances.size())
        unsqueeze_dim = (num_dimensions + dim - 1) % num_dimensions

        weighted_distances = pairwise_distances * target_weights.unsqueeze(
            unsqueeze_dim,
        )
    else:
        weighted_distances = pairwise_distances

    return weighted_distances.min(
        dim=dim,
    )


def compute_distance_between_palettes(
    v: torch.tensor,
    w: torch.tensor,
    params: dict,
) -> torch.tensor:
    pairwise_distances = torch.cdist(
        v.float(),
        w.float(),
    )

    if params["palette_distance"] == "sum_pairwise_distances":
        return pairwise_distances.sum(dim=[1, 2])

    if params.get("apply_ramp_in_color_distance"):
        pairwise_distances = adjust_pairwise_distances(pairwise_distances, params)

    # The first score
    minimal_distances_for_w, indices_for_w = compute_min_of_weighted_color_distances(
        pairwise_distances,
        params,
        dim=-2,
    )

    # The second score, in order to make the distance symmetrical
    minimal_distances_for_v, indices_for_v = compute_min_of_weighted_color_distances(
        pairwise_distances,
        params,
        dim=-1,
    )

    if params["palette_distance"] == "hausdorff_distance":
        return (
            torch.stack(
                (
                    minimal_distances_for_w.max(dim=1).to_numpy(),
                    minimal_distances_for_v.max(dim=1).to_numpy(),
                ),
            )
            .max(dim=0)
            .to_numpy()
        )

    score_for_w = to_score(minimal_distances_for_w, indices_for_w, params)
    score_for_v = to_score(minimal_distances_for_v, indices_for_v, params)

    if params["palette_distance"] == "modified_hausdorff_distance":
        return torch.stack((score_for_w, score_for_v)).max(dim=0).to_numpy()

    return score_for_w + score_for_v
