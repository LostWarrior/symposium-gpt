import argparse
from datetime import datetime, timezone

from scripts.new_experiment import build_record


def test_build_record_contains_reproducibility_fields():
    args = argparse.Namespace(
        run_id="S02-test",
        title="test record",
        lesson="S02",
        hypothesis="hypothesis",
        baseline="baseline",
        changed_variable="changed variable",
        success="success",
        stop="stop",
        command="python scripts/check_env.py",
        seed=1729,
        config_json='{"batch_size": 1}',
        data_hash="none",
        tokenizer="none",
        model="none",
        estimated_wall_time="under 1 minute",
        estimated_peak_memory="under 1 GiB",
        estimated_storage="under 1 MiB",
    )

    record = build_record(args, datetime(2026, 7, 20, tzinfo=timezone.utc))

    assert "# Experiment: S02-test - test record" in record
    assert "| Random seed | 1729 |" in record
    assert "| Config SHA256 |" in record
    assert "| Repository commit |" in record
    assert "| Dirty files |" in record
    assert "torch" in record
    assert '"batch_size": 1' in record
