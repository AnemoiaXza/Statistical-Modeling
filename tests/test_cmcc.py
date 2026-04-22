from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.cmcc import annualize_total_emissions
from stat_modeling.data.cmcc import build_resolved_annualized_panel
from stat_modeling.data.cmcc import build_match_candidates
from stat_modeling.data.cmcc import normalize_city_name_for_match


def test_normalize_city_name_for_match_handles_known_variants():
    assert normalize_city_name_for_match("Daxing'anling") == "da hinggan ling"
    assert normalize_city_name_for_match("Ma'anshan") == "ma anshan"
    assert normalize_city_name_for_match("Börtala Mongol") == "börtala"


def test_build_match_candidates_marks_direct_normalized_and_ambiguous_matches():
    cmcc_cities = ["Beijing", "Daxing'anling", "Baoji", "Baoding", "Amsterdam", "Ürümqi"]
    pku_reference = pd.DataFrame(
        [
            {"pref_name_year18_eng": "Beijing", "pref_name_year18": "北京市", "pref_code_year18": 1100},
            {
                "pref_name_year18_eng": "Da Hinggan Ling ",
                "pref_name_year18": "大兴安岭地区",
                "pref_code_year18": 2327,
            },
            {"pref_name_year18_eng": "baoji", "pref_name_year18": "保定市", "pref_code_year18": 1306},
            {"pref_name_year18_eng": "baoji", "pref_name_year18": "宝鸡市", "pref_code_year18": 6103},
            {"pref_name_year18_eng": "Urumqi", "pref_name_year18": "乌鲁木齐市", "pref_code_year18": 6501},
        ]
    )

    result = build_match_candidates(cmcc_cities=cmcc_cities, pku_reference=pku_reference)

    by_city = result.set_index("cmcc_city")
    assert by_city.loc["Beijing", "match_status"] == "direct"
    assert by_city.loc["Daxing'anling", "match_status"] == "normalized_candidate"
    assert by_city.loc["Baoji", "match_status"] == "manual_alias"
    assert by_city.loc["Baoding", "match_status"] == "manual_alias"
    assert by_city.loc["Ürümqi", "match_status"] == "manual_alias"
    assert by_city.loc["Amsterdam", "match_status"] == "unmatched"


def test_annualize_total_emissions_filters_incomplete_years():
    frame = pd.DataFrame(
        [
            {"city": "Beijing", "date": "2020-01-01", "sector": "Total", "value": 2.0},
            {"city": "Beijing", "date": "2020-01-02", "sector": "Total", "value": 3.0},
            {"city": "Beijing", "date": "2020-01-01", "sector": "Power", "value": 99.0},
            {"city": "Beijing", "date": "2021-01-01", "sector": "Total", "value": 4.0},
        ]
    )

    result = annualize_total_emissions(frame, expected_days_by_year={2020: 2, 2021: 365})

    assert list(result["year"]) == [2020]
    assert result.loc[result["year"] == 2020, "annual_total_value"].iat[0] == 5.0
    assert result.loc[result["year"] == 2020, "observed_days"].iat[0] == 2


def test_build_resolved_annualized_panel_attaches_pku_identifiers():
    annualized = pd.DataFrame(
        [
            {
                "city": "Ürümqi",
                "year": 2024,
                "annual_total_value": 100.0,
                "observed_days": 366,
                "expected_days": 366,
                "is_complete_year": True,
            }
        ]
    )
    matches = pd.DataFrame(
        [
            {
                "cmcc_city": "Ürümqi",
                "candidate_eng": "Urumqi",
                "candidate_cn": "乌鲁木齐市",
                "candidate_code": "6501",
                "match_status": "manual_alias",
                "is_obvious_foreign": False,
            }
        ]
    )

    result = build_resolved_annualized_panel(annualized=annualized, match_candidates=matches)

    assert result.loc[0, "pku_city_name_eng"] == "Urumqi"
    assert result.loc[0, "pku_city_name_cn"] == "乌鲁木齐市"
    assert result.loc[0, "pku_city_code"] == "6501"


def test_build_resolved_annualized_panel_excludes_obvious_foreign_rows():
    annualized = pd.DataFrame(
        [
            {
                "city": "Amsterdam",
                "year": 2024,
                "annual_total_value": 50.0,
                "observed_days": 366,
                "expected_days": 366,
                "is_complete_year": True,
            }
        ]
    )
    matches = pd.DataFrame(
        [
            {
                "cmcc_city": "Amsterdam",
                "candidate_eng": "Amsterdam",
                "candidate_cn": "阿姆斯特丹",
                "candidate_code": "9999",
                "match_status": "manual_alias",
                "is_obvious_foreign": True,
            }
        ]
    )

    result = build_resolved_annualized_panel(annualized=annualized, match_candidates=matches)

    assert result.empty
