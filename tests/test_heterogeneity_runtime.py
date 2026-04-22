from pathlib import Path
from subprocess import run


def test_heterogeneity_script_reports_dependency_status():
    result = run(
        ["python3", "src/05_heterogeneity.py", "--check-deps"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "econml=" in result.stdout
    assert "shap=" in result.stdout
