from pathlib import Path
from subprocess import run


def test_export_table_04_runs():
    repo = Path(__file__).resolve().parents[1]
    result = run(
        ["python3", "src/16_export_table_04.py"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert (repo / "outputs" / "tables" / "table_04_heterogeneity_candidate_city_extremes.csv").exists()
    assert (repo / "outputs" / "tables" / "table_04_heterogeneity_candidate_city_extremes.tex").exists()
