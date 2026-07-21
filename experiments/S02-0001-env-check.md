# Experiment: S02-0001-env-check - Environment check smoke record

## Status

- Date: 2026-07-20
- Status: proposed
- Course lesson: S02

## Question

- Hypothesis: The project environment can be verified repeatably.
- Baseline: Manual terminal checks.
- Single changed variable: Use scripts/check_env.py instead of manual commands.
- Success criterion: check_env.py passes in the learner terminal with MPS required.
- Stop criterion: Stop if package versions, Python version, or MPS availability mismatch.

## Reproducibility record

| Item | Value |
|---|---|
| Config SHA256 | 44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a |
| Random seed | 1729 |
| Data version/hash | none |
| Tokenizer/version | none |
| Model/version | none |
| Command | python scripts/check_env.py --require-mps |

## Environment

| Item | Value |
|---|---|
| Created UTC | 2026-07-20T20:29:27.916596+00:00 |
| Repository commit | d715ab6 |
| Dirty files | M .gitignore<br> M README.md<br>?? experiments/<br>?? scripts/new_experiment.py<br>?? tests/ |
| torch | 2.13.0 (expected 2.13.0) |
| numpy | 2.5.1 (expected 2.5.1) |
| psutil | 7.2.2 (expected 7.2.2) |
| pytest | 9.1.1 (expected 9.1.1) |

## Config

```json
{}
```

## Budget

- Estimated wall time: under 1 minute
- Actual wall time:
- Estimated peak memory: under 1 GiB
- Actual peak memory:
- Estimated storage: under 1 MiB
- Actual storage:

## Smoke test

- Command: `python scripts/check_env.py --require-mps`
- Expected signal: check_env.py passes in the learner terminal with MPS required.
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
