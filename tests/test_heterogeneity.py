from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.modeling.heterogeneity import build_heterogeneity_input
from stat_modeling.modeling.heterogeneity import compute_feature_correlation
from stat_modeling.modeling.heterogeneity import fit_candidate_cate
from stat_modeling.modeling.heterogeneity import parse_feature_columns


def test_parse_feature_columns_splits_comma_separated_values():
    assert parse_feature_columns("gdp_total, secondary_industry_share, fiscal_expenditure") == [
        "gdp_total",
        "secondary_industry_share",
        "fiscal_expenditure",
    ]


def test_build_heterogeneity_input_filters_missing_required_values():
    frame = pd.DataFrame(
        [
            {
                "year": 2023,
                "pku_city_code": 1100,
                "pku_city_name_cn": "北京市",
                "pku_city_name_eng": "Beijing",
                "digital_inclusive_finance_index": 1.0,
                "co2_emission_intensity": 2.0,
                "gdp_total": 3.0,
                "secondary_industry_share": 4.0,
            },
            {
                "year": 2023,
                "pku_city_code": 1200,
                "pku_city_name_cn": "天津市",
                "pku_city_name_eng": "Tianjin",
                "digital_inclusive_finance_index": 1.0,
                "co2_emission_intensity": None,
                "gdp_total": 3.0,
                "secondary_industry_share": 4.0,
            },
        ]
    )
    result = build_heterogeneity_input(
        frame,
        treatment_column="digital_inclusive_finance_index",
        outcome_column="co2_emission_intensity",
        feature_columns=["gdp_total", "secondary_industry_share"],
    )
    assert len(result) == 1


def test_compute_feature_correlation_returns_square_matrix():
    frame = pd.DataFrame({"gdp_total": [1, 2, 3], "fiscal_expenditure": [2, 4, 6]})
    result = compute_feature_correlation(frame, ["gdp_total", "fiscal_expenditure"])
    assert result.shape == (2, 2)


def test_fit_candidate_cate_runs_when_econml_is_available():
    try:
        import econml  # noqa: F401
    except Exception:
        return
    rng = pd.Series(range(120))
    frame = pd.DataFrame(
        {
            "year": [2023] * 120,
            "pku_city_code": rng % 30 + 1000,
            "pku_city_name_cn": [f"城市{i}" for i in range(120)],
            "pku_city_name_eng": [f"City{i}" for i in range(120)],
            "digital_inclusive_finance_index": rng * 0.1 + 1.0,
            "co2_emission_intensity": rng * -0.02 + 5.0,
            "gdp_total": rng * 1.0 + 100.0,
            "secondary_industry_share": rng * 0.01 + 20.0,
            "fiscal_expenditure": rng * 3.0 + 1000.0,
        }
    )
    cate_frame, summary = fit_candidate_cate(
        frame=frame,
        treatment_column="digital_inclusive_finance_index",
        outcome_column="co2_emission_intensity",
        feature_columns=["gdp_total", "secondary_industry_share", "fiscal_expenditure"],
        control_columns=["gdp_total", "secondary_industry_share", "fiscal_expenditure"],
    )
    assert len(cate_frame) == len(frame)
    assert summary.nobs == len(frame)
