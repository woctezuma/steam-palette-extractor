import torch


def normalize_weights(weights, dim=-1):
    return weights / torch.linalg.vector_norm(weights, ord=0, dim=dim, keepdim=True)


def to_weights(indices, factor):
    return torch.exp(factor * indices)
