import argparse
import importlib.metadata
import platform
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "requirements.txt"


def version(package: str) -> str:
    return importlib.metadata.version(package)


def expected_versions() -> dict[str, str]:
    expected: dict[str, str] = {}

    for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            raise SystemExit(f"unsupported requirement format: {line}")

        package, expected_version = line.split("==", 1)
        expected[package] = expected_version

    return expected


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Symposium-GPT local env.")
    parser.add_argument(
        "--require-mps",
        action="store_true",
        help="Fail if PyTorch cannot allocate a tensor on Apple MPS.",
    )
    args = parser.parse_args()

    print(f"python: {platform.python_version()}")
    print(f"executable: {sys.executable}")

    if sys.version_info[:2] != (3, 12):
        raise SystemExit("expected Python 3.12")

    for package, expected in expected_versions().items():
        actual = version(package)
        print(f"{package}: {actual}")
        if actual != expected:
            raise SystemExit(f"{package} version mismatch: {actual} != {expected}")

    import torch

    print(f"mps built: {torch.backends.mps.is_built()}")
    print(f"mps available: {torch.backends.mps.is_available()}")

    cpu_tensor = torch.ones(4, device="cpu")
    print(f"cpu tensor: {cpu_tensor}")

    if torch.backends.mps.is_available():
        mps_tensor = torch.ones(4, device="mps")
        print(f"mps tensor: {mps_tensor}")
    elif args.require_mps:
        raise SystemExit("MPS is required but not available")

    print("environment check passed")


if __name__ == "__main__":
    main()
