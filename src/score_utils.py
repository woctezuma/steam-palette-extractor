import torch


def normalize_indices(indices, min_value=None, max_value=None):
    if min_value is None:
        min_value = indices.min()
    if max_value is None:
        max_value = indices.max()
    return (indices - min_value) / (max_value - min_value)


def normalize_weights(weights):
    return weights / torch.linalg.vector_norm(weights, ord=0, dim=-1, keepdim=True)


def to_weights(indices, factor, exponent):
    return (1 + factor * indices) ** exponent


def to_weights_source(indices_source, params, num_columns):
    # The following normalized values lie between 0 and 1.
    normalized_indices_source = indices_source / (num_columns - 1)
    rank_weights_source = to_weights(
        normalized_indices_source,
        params["factor_source"],
        params["exponent_source"],
    )
    return normalize_weights(rank_weights_source)


def to_weights_delta(indices_target, indices_source, params, num_columns, threshold=0):
    delta_indices = indices_target - indices_source

    # The following normalized values lie between -1 and 1.
    normalized_delta_indices = delta_indices / (num_columns - 1)

    # Threshold, to ensure that there is no penalty when the matched color has
    # a lower index in the target palette than the color in the source palette.
    normalized_delta_indices[normalized_delta_indices < threshold] = 0

    return to_weights(
        normalized_delta_indices,
        params["factor_ramp"],
        params["exponent_ramp"],
    )


def to_score(
    minimal_distances: torch.tensor,
    indices: torch.tensor,
    params: dict,
) -> torch.tensor:
    num_columns = len(indices[0])
    indices_source = torch.tensor(range(num_columns))
    rank_weights_source = to_weights_source(indices_source, params, num_columns)
    score = minimal_distances * rank_weights_source

    rank_weights_target = to_weights(
        indices,
        params["factor_target"],
        params["exponent_target"],
    )
    score *= rank_weights_target

    ramp_weights = to_weights_delta(indices, indices_source, params, num_columns)
    score *= ramp_weights
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
