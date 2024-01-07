import torch


def to_score(
    minimal_distances: torch.tensor,
    indices: torch.tensor,
    params: dict,
) -> torch.tensor | float:
    factor = params["factor"]
    exponent = params["exponent"]

    rank_weights = (1 + factor * indices) ** exponent
    score = minimal_distances * rank_weights
    return score.sum(dim=1) if len(score.size()) > 1 else score.sum().item()


def compute_distance_between_palettes(
    v: torch.tensor,
    w: torch.tensor,
    params: dict,
) -> torch.tensor | float:
    pairwise_distances = torch.cdist(
        v.float(),
        w.float(),
    )

    # The first score
    minimal_distances, indices = pairwise_distances.min(
        dim=len(pairwise_distances.size()) - 2,
    )
    score_for_w = to_score(minimal_distances, indices, params)

    # The second score, in order to make the distance symmetrical
    minimal_distances, indices = pairwise_distances.min(
        dim=len(pairwise_distances.size()) - 1,
    )
    score_for_v = to_score(minimal_distances, indices, params)

    return score_for_w + score_for_v
