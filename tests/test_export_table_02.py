from pathlib import Path
from subprocess import run


def test_export_table_02_runs(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    source = repo / "outputs" / "tables" / "table_02_dml_main_and_robustness.csv"
    if not source.exists():
        source.write_text(
            "outcome_label_cn,ate,std_error,ci_lower,ci_upper,p_value,nobs\n碳排放强度,-0.1,0.01,-0.2,-0.01,0.03,100\n",
            encoding="utf-8",
        )
    result = run(
        ["python3", "src/14_export_table_02.py"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert (repo / "outputs" / "tables" / "table_02_dml_main_and_robustness.tex").exists()
