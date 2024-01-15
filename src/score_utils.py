import torch

from src.weight_utils import normalize_weights, to_weights


def to_weights_source(indices_source, params, num_columns):
    # The following normalized values lie between 0 and 1.
    normalized_indices_source = indices_source / (num_columns - 1)
    rank_weights_source = to_weights(
        normalized_indices_source,
        params["factor_source"],
    )
    return normalize_weights(rank_weights_source)


def to_weights_delta(indices_target, indices_source, params, num_columns):
    delta_indices = indices_target - indices_source

    # The following normalized values lie between -1 and 1.
    normalized_delta_indices = delta_indices / (num_columns - 1)

    # Threshold, to ensure that there is no penalty when the matched color has
    # a lower index in the target palette than the color in the source palette.
    threshold = params.get("threshold_ramp")
    if threshold is not None:
        normalized_delta_indices[normalized_delta_indices < threshold] = 0

    return to_weights(
        normalized_delta_indices,
        params["factor_ramp"],
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
    ramp_weights = to_weights_delta(
        indices,
        indices_source,
        params,
        num_columns,
    )
    score *= ramp_weights
    return score.sum(dim=1) if len(score.size()) > 1 else score.sum()
