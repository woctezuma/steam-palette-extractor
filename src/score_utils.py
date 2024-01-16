import torch

from src.weight_utils import to_weights_delta, to_weights_source, to_weights_target


def to_score(
    minimal_distances: torch.tensor,
    indices: torch.tensor,
    params: dict,
) -> torch.tensor:
    num_columns = len(indices[0])
    indices_source = torch.tensor(range(num_columns))
    rank_weights_source = to_weights_source(indices_source, params, num_columns)
    score = minimal_distances * rank_weights_source
    if params.get("apply_target_in_palette_distance"):
        rank_weights_target = to_weights_target(indices, params, num_columns)
        score *= rank_weights_target
    if params.get("apply_ramp_in_palette_distance"):
        ramp_weights = to_weights_delta(
            indices,
            indices_source,
            params,
            num_columns,
        )
        score *= ramp_weights
    return score.sum(dim=1) if len(score.size()) > 1 else score.sum()
