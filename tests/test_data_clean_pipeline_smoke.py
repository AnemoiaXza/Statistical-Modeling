from pathlib import Path
from subprocess import run


def test_data_clean_script_runs_with_help():
    result = run(
        ["python3", "src/01_data_clean.py", "--help"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "usage" in result.stdout.lower()
