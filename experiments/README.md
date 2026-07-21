# Experiments

Every run gets a record before it becomes expensive.

Required fields:

- question and hypothesis;
- baseline;
- single changed variable;
- success and stop criteria;
- seed;
- command;
- git revision and dirty files;
- package versions from `requirements.txt`;
- hardware and OS snapshot;
- data, tokenizer, and model identity.

Create a record:

```bash
python scripts/new_experiment.py \
  --run-id S02-0001-env-check \
  --title "Environment check smoke record" \
  --lesson S02 \
  --hypothesis "The project environment can be verified repeatably." \
  --baseline "Manual terminal checks." \
  --changed-variable "Use scripts/check_env.py instead of manual commands." \
  --success "check_env.py passes in the learner terminal with MPS required." \
  --stop "Stop if package versions, Python version, or MPS availability mismatch." \
  --command "python scripts/check_env.py --require-mps"
```
