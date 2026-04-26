from pathlib import Path
from subprocess import run


def test_export_table_03_runs():
    repo = Path(__file__).resolve().parents[1]
    result = run(
        ["python3", "src/15_export_table_03.py"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert (repo / "outputs" / "tables" / "table_03_heterogeneity_candidate_summary.csv").exists()
    assert (repo / "outputs" / "tables" / "table_03_heterogeneity_candidate_summary.tex").exists()
