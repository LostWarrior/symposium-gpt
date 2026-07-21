import argparse

import torch

def make_pair(seed: int, size: int) -> tuple[torch.Tensor, torch.Tensor]:
    torch.manual_seed(seed)
    first = torch.randn(size)

    torch.manual_seed(seed)
    second = torch.randn(size)

    return first, second


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1729)
    parser.add_argument("--size", type=int, default=4)
    args = parser.parse_args()

    first,second = make_pair(args.seed, args.size)

    print("seed:", args.seed)
    print("size:", args.size)
    print("first:", first)
    print("second:", second)
    print("equal:", torch.equal(first, second))


if __name__ == "__main__":
    main()



