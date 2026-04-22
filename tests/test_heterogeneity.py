from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.modeling.heterogeneity import build_heterogeneity_input
from stat_modeling.modeling.heterogeneity import compute_feature_correlation
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
