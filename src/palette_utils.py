import torch

from src.score_utils import to_score


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

    # The first score
    minimal_distances_for_w, indices_for_w = pairwise_distances.min(
        dim=-2,
    )

    # The second score, in order to make the distance symmetrical
    minimal_distances_for_v, indices_for_v = pairwise_distances.min(
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
