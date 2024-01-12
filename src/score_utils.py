import torch


def to_weights(indices, factor, exponent):
    return (1 + factor * indices) ** exponent


def to_score(
    minimal_distances: torch.tensor,
    indices: torch.tensor,
    params: dict,
) -> torch.tensor:
    rank_weights = to_weights(indices, params["factor"], params["exponent"])
    score = minimal_distances * rank_weights
    return score.sum(dim=1) if len(score.size()) > 1 else score.sum()


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
        dim=len(pairwise_distances.size()) - 2,
    )

    # The second score, in order to make the distance symmetrical
    minimal_distances_for_v, indices_for_v = pairwise_distances.min(
        dim=len(pairwise_distances.size()) - 1,
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
