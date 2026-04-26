from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.pku import build_pku_cmcc_candidate_panel
from stat_modeling.data.pku import load_pku_prefecture_panel


def test_load_pku_prefecture_panel_applies_code_based_english_name_overrides(tmp_path):
    source = tmp_path / "pku.xlsx"
    frame = pd.DataFrame(
        [
            {
                "year": 2023,
                "pref_name_year18": "保定市",
                "pref_name_year18_eng": "baoji",
                "pref_code_year18": 1306,
                "index_aggregate": 1.0,
                "coverage_breadth": 1.0,
                "usage_depth": 1.0,
                "payment": 1.0,
                "insurance": 1.0,
                "monetary_fund": 1.0,
                "investment": 1.0,
                "credit": 1.0,
                "credit_investigation": 1.0,
                "digitization_level": 1.0,
            }
        ]
    )
    with pd.ExcelWriter(source) as writer:
        frame.to_excel(writer, sheet_name="Prefecture_Level_Cities", index=False)

    result = load_pku_prefecture_panel(source, year_min=2023, year_max=2023)

    assert result.loc[0, "pku_city_name_eng"] == "Baoding"


def test_build_pku_cmcc_candidate_panel_joins_by_code_and_year():
    pku_panel = pd.DataFrame(
        [
            {"year": 2023, "pku_city_code": 1100, "pku_city_name_cn": "北京市", "pku_city_name_eng": "Beijing"},
            {"year": 2023, "pku_city_code": 1200, "pku_city_name_cn": "天津市", "pku_city_name_eng": "Tianjin"},
        ]
    )
    cmcc_resolved = pd.DataFrame(
        [
            {
                "year": 2023,
                "pku_city_code": "1100",
                "pku_city_name_cn": "北京市",
                "city": "Beijing",
                "annual_total_value": 100.0,
                "match_status": "direct",
            }
        ]
    )

    result = build_pku_cmcc_candidate_panel(pku_panel, cmcc_resolved, year_min=2023, year_max=2023)

    assert bool(result.loc[result["pku_city_code"] == 1100, "has_cmcc_outcome"].iat[0]) is True
    assert bool(result.loc[result["pku_city_code"] == 1200, "has_cmcc_outcome"].iat[0]) is False
