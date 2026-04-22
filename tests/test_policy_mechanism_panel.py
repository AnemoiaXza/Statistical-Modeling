from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.mechanism_panel import build_policy_mechanism_template
from stat_modeling.policy_text.mechanism_panel import merge_policy_mechanism


def test_build_policy_mechanism_template_creates_city_year_keys():
    base = pd.DataFrame(
        [
            {"year": 2023, "pku_city_code": 1100, "pku_city_name_cn": "北京市"},
            {"year": 2023, "pku_city_code": 1200, "pku_city_name_cn": "天津市"},
        ]
    )
    result = build_policy_mechanism_template(base)
    assert len(result) == 2
    assert "policy_strength" in result.columns


def test_merge_policy_mechanism_attaches_mechanism_columns():
    base = pd.DataFrame(
        [
            {"year": 2023, "pku_city_code": 1100, "pku_city_name_cn": "北京市", "value": 1},
        ]
    )
    mechanism = pd.DataFrame(
        [
            {
                "year": 2023,
                "pku_city_code": 1100,
                "pku_city_name_cn": "北京市",
                "policy_strength": 3.0,
                "execution_clarity": 4.0,
                "digital_green_synergy": 5.0,
                "policy_doc_count": 10,
                "mechanism_data_status": "ready",
            }
        ]
    )
    result = merge_policy_mechanism(base, mechanism)
    assert result.loc[0, "policy_strength"] == 3.0
