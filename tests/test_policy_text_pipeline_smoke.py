from pathlib import Path
from subprocess import run


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_policy_text_script_runs_with_help():
    result = run(
        ["python3", "src/08_policy_text.py", "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "usage" in result.stdout.lower()
    assert "mechanism/moderation" in result.stdout.lower()


def test_policy_text_script_writes_dry_run_summary():
    summary_name = "policy_text_pipeline_smoke.txt"
    summary_path = REPO_ROOT / "logs" / "policy_text" / summary_name
    if summary_path.exists():
        summary_path.unlink()

    result = run(
        [
            "python3",
            "src/08_policy_text.py",
            "--stage",
            "discover",
            "--dry-run",
            "--summary-name",
            summary_name,
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    try:
        assert result.returncode == 0
        assert summary_path.exists()
        summary_text = summary_path.read_text(encoding="utf-8")
        assert "mechanism/moderation only" in summary_text
        assert "stage: discover" in summary_text
    finally:
        if summary_path.exists():
            summary_path.unlink()
