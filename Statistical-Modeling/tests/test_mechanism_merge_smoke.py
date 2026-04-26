from pathlib import Path
from subprocess import run


def test_mechanism_merge_script_runs():
    result = run(
        ["python3", "src/22_build_modeling_policy_seed_panel.py"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
