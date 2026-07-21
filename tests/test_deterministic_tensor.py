import torch
from scripts.deterministic_tensor import make_pair


def test_same_seed_same_tensor():
    first, second = make_pair(seed=1729, size=4)

    assert torch.equal(first, second)

