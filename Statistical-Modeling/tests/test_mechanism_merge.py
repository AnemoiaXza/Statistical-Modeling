from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.mechanism_merge import merge_modeling_with_policy_seed


def test_merge_modeling_with_policy_seed_keeps_one_to_one_panel():
    modeling = pd.DataFrame(
        [
            {"year": 2021, "pku_city_code": 1100, "pku_city_name_cn": "北京市", "x": 1},
            {"year": 2021, "pku_city_code": 1200, "pku_city_name_cn": "天津市", "x": 2},
        ]
    )
    mechanism = pd.DataFrame(
        [
            {"year": 2021, "pku_city_code": 1100, "pku_city_name_cn": "北京市", "policy_doc_count": 2},
            {"year": 2021, "pku_city_code": 1200, "pku_city_name_cn": "天津市", "policy_doc_count": 2},
        ]
    )
    result = merge_modeling_with_policy_seed(modeling, mechanism)
    assert len(result) == 2
    assert result.loc[result["pku_city_code"] == 1100, "policy_doc_count"].iat[0] == 2
