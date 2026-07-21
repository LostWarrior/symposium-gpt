import argparse
import hashlib
import importlib.metadata
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import psutil


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "requirements.txt"
EXPERIMENTS = ROOT / "experiments"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return f"unavailable: {result.stderr.strip()}"
    return result.stdout.strip()


def requirement_versions() -> dict[str, str]:
    versions: dict[str, str] = {}

    for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            raise SystemExit(f"unsupported requirement format: {line}")

        package, expected = line.split("==", 1)
        try:
            actual = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            actual = "not installed"
        versions[package] = f"{actual} (expected {expected})"

    return versions


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def markdown_table(rows: dict[str, str]) -> str:
    lines = ["| Item | Value |", "|---|---|"]
    for key, value in rows.items():
        safe_value = value.replace("\n", "<br>")
        lines.append(f"| {key} | {safe_value} |")
    return "\n".join(lines)


def build_record(args: argparse.Namespace, created_at: datetime | None = None) -> str:
    if not RUN_ID_RE.match(args.run_id):
        raise SystemExit("run ID must use only letters, numbers, '.', '_', and '-'")

    created_at = created_at or datetime.now(timezone.utc)
    config = json.loads(args.config_json)
    config_text = json.dumps(config, sort_keys=True, indent=2)
    dirty = run_git(["status", "--short"]) or "clean"
    commit = run_git(["rev-parse", "--short", "HEAD"])

    env_rows = {
        "Created UTC": created_at.isoformat(),
        "Repository commit": commit,
        "Dirty files": dirty,
    }
    env_rows.update(requirement_versions())

    repro_rows = {
        "Config SHA256": sha256_text(config_text),
        "Random seed": str(args.seed),
        "Data version/hash": args.data_hash,
        "Tokenizer/version": args.tokenizer,
        "Model/version": args.model,
        "Command": args.command,
    }

    return f"""# Experiment: {args.run_id} - {args.title}

## Status

- Date: {created_at.date().isoformat()}
- Status: proposed
- Course lesson: {args.lesson}

## Question

- Hypothesis: {args.hypothesis}
- Baseline: {args.baseline}
- Single changed variable: {args.changed_variable}
- Success criterion: {args.success}
- Stop criterion: {args.stop}

## Reproducibility record

{markdown_table(repro_rows)}

## Environment

{markdown_table(env_rows)}

## Config

```json
{config_text}
```

## Budget

- Estimated wall time: {args.estimated_wall_time}
- Actual wall time:
- Estimated peak memory: {args.estimated_peak_memory}
- Actual peak memory:
- Estimated storage: {args.estimated_storage}
- Actual storage:

## Smoke test

- Command: `{args.command}`
- Expected signal: {args.success}
- Result:
- Safe to continue? yes | no

## Results

| Metric | Baseline | Treatment | Difference |
|---|---:|---:|---:|

Representative outputs and failure cases:

## Interpretation

- Does result support hypothesis?
- Plausible alternative explanations:
- Anomalies:

## Decision

- Adopt | reject | repeat | inconclusive:
- Confidence:
- Revisit trigger:
- Next smallest experiment:

## Artifact ledger

| Artifact | Path/URL | Hash/version | Keep? |
|---|---|---|---|
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a reproducible experiment record.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--lesson", required=True)
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--changed-variable", required=True)
    parser.add_argument("--success", required=True)
    parser.add_argument("--stop", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--seed", type=int, default=1729)
    parser.add_argument("--config-json", default="{}")
    parser.add_argument("--data-hash", default="none")
    parser.add_argument("--tokenizer", default="none")
    parser.add_argument("--model", default="none")
    parser.add_argument("--estimated-wall-time", default="under 1 minute")
    parser.add_argument("--estimated-peak-memory", default="under 1 GiB")
    parser.add_argument("--estimated-storage", default="under 1 MiB")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    record = build_record(args)
    path = EXPERIMENTS / f"{args.run_id}.md"

    if args.dry_run:
        print(record)
        return

    if path.exists() and not args.force:
        raise SystemExit(f"experiment record already exists: {path}")

    EXPERIMENTS.mkdir(parents=True, exist_ok=True)
    path.write_text(record, encoding="utf-8")
    print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
