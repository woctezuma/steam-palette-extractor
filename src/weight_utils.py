import torch


def normalize_weights(weights, dim=-1):
    return weights / torch.linalg.vector_norm(weights, ord=0, dim=dim, keepdim=True)


def to_weights(indices, factor):
    return torch.exp(factor * indices)


def to_weights_source(indices_source, params, num_elements):
    # The following normalized values lie between 0 and 1.
    normalized_indices_source = indices_source / (num_elements - 1)
    rank_weights_source = to_weights(
        normalized_indices_source,
        params["factor_source"],
    )
    return normalize_weights(rank_weights_source)


def to_weights_delta(indices_target, indices_source, params, num_elements):
    delta_indices = indices_target - indices_source

    # The following normalized values lie between -1 and 1.
    normalized_delta_indices = delta_indices / (num_elements - 1)

    # Threshold, to ensure that there is no penalty when the matched color has
    # a lower index in the target palette than the color in the source palette.
    threshold = params.get("threshold_ramp")
    if threshold is not None:
        normalized_delta_indices[normalized_delta_indices < threshold] = 0

    return to_weights(
        normalized_delta_indices,
        params["factor_ramp"],
    )


def to_weights_target(indices_target, params, num_elements):
    # The following normalized values lie between 0 and 1.
    normalized_indices_target = indices_target / (num_elements - 1)

    return to_weights(
        normalized_indices_target,
        params["factor_target"],
    )
