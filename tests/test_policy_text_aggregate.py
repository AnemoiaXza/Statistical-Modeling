from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.aggregate import aggregate_policy_scores
from stat_modeling.policy_text.aggregate import assign_documents_to_cities


def test_assign_and_aggregate_policy_scores():
    documents = pd.DataFrame(
        [
            {
                "admin_level": "central",
                "region_name": "China",
                "pub_date": "2024-01-01",
                "policy_strength": 3.0,
                "execution_clarity": 4.0,
                "digital_green_synergy": 5.0,
            },
            {
                "admin_level": "provincial",
                "region_name": "浙江省",
                "pub_date": "2024-02-01",
                "policy_strength": 2.0,
                "execution_clarity": 3.0,
                "digital_green_synergy": 4.0,
            },
        ]
    )
    cities = pd.DataFrame(
        [
            {"city_name_cn": "杭州市", "province_name_cn": "浙江省", "year": 2024},
            {"city_name_cn": "广州市", "province_name_cn": "广东省", "year": 2024},
        ]
    )

    assigned = assign_documents_to_cities(documents, cities)
    aggregated = aggregate_policy_scores(assigned)

    hangzhou = aggregated.loc[aggregated["city_name_cn"] == "杭州市"].iloc[0]
    guangzhou = aggregated.loc[aggregated["city_name_cn"] == "广州市"].iloc[0]

    assert hangzhou["sum_policy_strength_city_year"] == 5.0
    assert guangzhou["sum_policy_strength_city_year"] == 3.0
