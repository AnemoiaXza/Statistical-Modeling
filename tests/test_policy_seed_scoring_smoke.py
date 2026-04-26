from pathlib import Path
from subprocess import run


def test_policy_seed_scoring_script_runs():
    result = run(
        ["python3", "src/20_score_policy_seeds.py"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
