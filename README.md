# symposium-gpt

Local model research project for the voice-enabled philosophy companion.

## Environment

Use the project venv:

```bash
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Check packages and MPS:

```bash
python scripts/check_env.py --require-mps
```

## Experiments

Create a reproducible experiment record before running training or benchmarks:

```bash
python scripts/new_experiment.py --help
```
