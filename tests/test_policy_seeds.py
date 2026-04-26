from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.seeds import build_seed_city_year_doc_counts
from stat_modeling.policy_text.seeds import build_seed_registry_frame


def test_build_seed_registry_frame_returns_central_documents():
    frame = build_seed_registry_frame()
    assert len(frame) >= 3
    assert set(frame["admin_level"]) == {"central"}
    assert "has_quant_target" in frame.columns


def test_build_seed_city_year_doc_counts_assigns_central_docs_to_all_cities():
    registry = build_seed_registry_frame()
    template = pd.DataFrame(
        [
            {"year": 2021, "pku_city_code": 1100, "pku_city_name_cn": "北京市"},
            {"year": 2024, "pku_city_code": 1200, "pku_city_name_cn": "天津市"},
        ]
    )
    result = build_seed_city_year_doc_counts(registry, template)
    assert result["policy_doc_count_seeded"].sum() >= 2
