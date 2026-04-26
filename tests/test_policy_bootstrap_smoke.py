from pathlib import Path
from subprocess import run


def test_policy_bootstrap_script_runs():
    result = run(
        ["python3", "src/18_prepare_policy_text_bootstrap.py"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
