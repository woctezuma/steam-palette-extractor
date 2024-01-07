import torch


def get_most_similar_app_ids(
    distances: torch.tensor,
    pre_computed_app_ids: list[str],
    topk: int = 0,
) -> tuple[list[str], list[int]]:
    if topk > 0:
        indices = torch.topk(distances, k=topk, largest=False)
    else:
        indices = torch.argsort(distances)
    return [pre_computed_app_ids[i] for i in indices], indices


def get_ground_truth_rank(
    ground_truth_app_id: None | int,
    most_similar_app_ids: list[str],
    verbose=True,
) -> None | int:
    if ground_truth_app_id:
        try:
            rank = 1 + most_similar_app_ids.index(str(ground_truth_app_id))
            if verbose:
                print(
                    f"Ground truth (appID = {ground_truth_app_id}) is ranked n°{rank}.",
                )
        except ValueError:
            rank = None
            if verbose:
                print(
                    f"Ground truth (appID = {ground_truth_app_id}) is not ranked.",
                )
    else:
        rank = None

    return rank


def get_ground_truth_ranks(
    ground_truth_app_ids: list[None | int],
    most_similar_app_ids: list[str],
    verbose=True,
) -> list[int]:
    ground_truth_ranks = []
    for app_id in ground_truth_app_ids:
        rank = get_ground_truth_rank(app_id, most_similar_app_ids, verbose)

        if rank:
            ground_truth_ranks.append(rank)

    return ground_truth_ranks
