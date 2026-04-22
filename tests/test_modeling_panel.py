from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.modeling_panel import build_modeling_candidate_panel


def test_build_modeling_candidate_panel_marks_rows_ready_when_outcome_and_controls_exist():
    pku_cmcc = pd.DataFrame(
        [
            {"pku_city_code": 1100, "pku_city_name_cn": "北京市", "year": 2023, "has_cmcc_outcome": True},
            {"pku_city_code": 1200, "pku_city_name_cn": "天津市", "year": 2023, "has_cmcc_outcome": False},
        ]
    )
    controls = pd.DataFrame(
        [
            {
                "pku_city_code": 1100,
                "year": 2023,
                "gdp_total": 1.0,
                "secondary_industry_share": 2.0,
                "population_raw": 3.0,
                "fiscal_expenditure": 4.0,
            },
            {
                "pku_city_code": 1200,
                "year": 2023,
                "gdp_total": 1.0,
                "secondary_industry_share": 2.0,
                "population_raw": 3.0,
                "fiscal_expenditure": 4.0,
            },
        ]
    )

    result = build_modeling_candidate_panel(pku_cmcc, controls)

    assert bool(result.loc[result["pku_city_code"] == 1100, "ready_for_dml_candidate"].iat[0]) is True
    assert bool(result.loc[result["pku_city_code"] == 1200, "ready_for_dml_candidate"].iat[0]) is False


def test_build_modeling_candidate_panel_preserves_unique_city_year_keys():
    pku_cmcc = pd.DataFrame(
        [
            {"pku_city_code": 1100, "pku_city_name_cn": "北京市", "year": 2023, "has_cmcc_outcome": True},
            {"pku_city_code": 1200, "pku_city_name_cn": "天津市", "year": 2023, "has_cmcc_outcome": True},
        ]
    )
    controls = pd.DataFrame(
        [
            {"pku_city_code": 1100, "year": 2023, "gdp_total": 1, "secondary_industry_share": 2, "population_raw": 3, "fiscal_expenditure": 4},
            {"pku_city_code": 1200, "year": 2023, "gdp_total": 1, "secondary_industry_share": 2, "population_raw": 3, "fiscal_expenditure": 4},
        ]
    )
    result = build_modeling_candidate_panel(pku_cmcc, controls)
    assert result.groupby(["pku_city_code", "year"]).size().max() == 1


def test_build_modeling_candidate_panel_raises_on_duplicate_control_keys():
    pku_cmcc = pd.DataFrame(
        [{"pku_city_code": 1100, "pku_city_name_cn": "北京市", "year": 2023, "has_cmcc_outcome": True}]
    )
    controls = pd.DataFrame(
        [
            {"pku_city_code": 1100, "year": 2023, "gdp_total": 1, "secondary_industry_share": 2, "population_raw": 3, "fiscal_expenditure": 4},
            {"pku_city_code": 1100, "year": 2023, "gdp_total": 1, "secondary_industry_share": 2, "population_raw": 3, "fiscal_expenditure": 4},
        ]
    )
    try:
        build_modeling_candidate_panel(pku_cmcc, controls)
        assert False, "expected duplicate key error"
    except ValueError as exc:
        assert "Duplicate core control keys" in str(exc)
