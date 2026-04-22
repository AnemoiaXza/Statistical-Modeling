from pathlib import Path
from subprocess import run


def test_policy_mechanism_template_script_runs():
    result = run(
        ["python3", "src/17_prepare_policy_mechanism_template.py"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
