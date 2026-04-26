from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.dml_input import build_dml_candidate_input


def test_build_dml_candidate_input_filters_ready_rows_and_computes_intensity():
    panel = pd.DataFrame(
        [
            {
                "year": 2023,
                "pku_city_code": 1100,
                "pku_city_name_cn": "北京市",
                "pku_city_name_eng": "Beijing",
                "digital_inclusive_finance_index": 1.0,
                "dfi_coverage_breadth": 2.0,
                "dfi_usage_depth": 3.0,
                "dfi_digitization_level": 4.0,
                "co2_emission_total": 100.0,
                "gdp_total": 20.0,
                "secondary_industry_share": 30.0,
                "population_raw": 40.0,
                "fiscal_expenditure": 50.0,
                "match_status": "direct",
                "ready_for_dml_candidate": True,
            },
            {
                "year": 2023,
                "pku_city_code": 1200,
                "pku_city_name_cn": "天津市",
                "pku_city_name_eng": "Tianjin",
                "digital_inclusive_finance_index": 1.0,
                "dfi_coverage_breadth": 2.0,
                "dfi_usage_depth": 3.0,
                "dfi_digitization_level": 4.0,
                "co2_emission_total": 100.0,
                "gdp_total": 20.0,
                "secondary_industry_share": 30.0,
                "population_raw": 40.0,
                "fiscal_expenditure": 50.0,
                "match_status": "direct",
                "ready_for_dml_candidate": False,
            },
        ]
    )

    result = build_dml_candidate_input(panel)

    assert len(result) == 1
    assert result.loc[0, "co2_emission_intensity"] == 5.0
