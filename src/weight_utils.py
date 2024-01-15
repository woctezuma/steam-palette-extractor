import torch


def scale_indices(indices, num_elements):
    return indices / (num_elements - 1)


def normalize_weights(weights, dim=-1):
    return weights / torch.linalg.vector_norm(weights, ord=0, dim=dim, keepdim=True)


def to_weights(indices, factor):
    return torch.exp(factor * indices)


def to_weights_wrapper(indices, factor, num_elements):
    # The following normalized values lie between 0 and 1.
    normalized_indices = scale_indices(indices, num_elements)

    return to_weights(
        normalized_indices,
        factor,
    )


def to_weights_target(indices_target, params, num_elements):
    return to_weights_wrapper(indices_target, params["factor_target"], num_elements)


def to_weights_source(indices_source, params, num_elements):
    rank_weights_source = to_weights_wrapper(
        indices_source,
        params["factor_source"],
        num_elements,
    )
    return normalize_weights(rank_weights_source)


def to_weights_delta(indices_target, indices_source, params, num_elements):
    delta_indices = indices_target - indices_source

    # The following normalized values lie between -1 and 1.
    normalized_delta_indices = scale_indices(delta_indices, num_elements)

    # Threshold, to ensure that there is no penalty when the matched color has
    # a lower index in the target palette than the color in the source palette.
    threshold = params.get("low_threshold_ramp")
    if threshold is not None:
        normalized_delta_indices[normalized_delta_indices < threshold] = threshold

    return to_weights(
        normalized_delta_indices,
        params["factor_ramp"],
    )
