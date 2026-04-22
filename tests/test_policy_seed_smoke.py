from pathlib import Path
from subprocess import run


def test_policy_seed_script_runs():
    result = run(
        ["python3", "src/19_seed_policy_registry.py"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
