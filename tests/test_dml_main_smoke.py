from pathlib import Path
from subprocess import run
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.io import write_table

def test_dml_main_script_runs_with_help():
    result = run(
        ["python3", "src/04_dml_main.py", "--help"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_dml_main_script_prepares_filtered_input(tmp_path):
    input_path = tmp_path / "dml_input.csv"
    output_path = tmp_path / "filtered.csv"
    frame = pd.DataFrame(
        [
            {
                "pku_city_code": 1100,
                "year": 2023,
                "digital_inclusive_finance_index": 1.0,
                "co2_emission_intensity": 2.0,
                "co2_emission_total": 3.0,
                "gdp_total": 4.0,
                "secondary_industry_share": 5.0,
            },
            {
                "pku_city_code": 1200,
                "year": 2023,
                "digital_inclusive_finance_index": 1.0,
                "co2_emission_intensity": None,
                "co2_emission_total": 3.0,
                "gdp_total": 4.0,
                "secondary_industry_share": 5.0,
            },
        ]
    )
    write_table(frame, input_path)

    result = run(
        [
            "python3",
            "src/04_dml_main.py",
            "--input-path",
            str(input_path),
            "--output-path",
            str(output_path),
            "--control-columns",
            "gdp_total,secondary_industry_share",
            "--summary-name",
            "tmp_dml_summary.txt",
        ],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert output_path.exists()
