from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.bootstrap import build_policy_city_year_scores_template
from stat_modeling.policy_text.bootstrap import build_policy_document_registry_template
from stat_modeling.policy_text.bootstrap import build_policy_source_manifest


def test_build_policy_source_manifest_seeds_core_sites():
    frame = build_policy_source_manifest()
    assert {"gov.cn", "ndrc.gov.cn", "mee.gov.cn"} <= set(frame["source_site"])


def test_build_policy_document_registry_template_has_expected_columns():
    frame = build_policy_document_registry_template()
    assert "policy_strength" in frame.columns
    assert "document_status" in frame.columns


def test_build_policy_city_year_scores_template_uses_modeling_keys():
    base = pd.DataFrame(
        [{"year": 2023, "pku_city_code": 1100, "pku_city_name_cn": "北京市"}]
    )
    frame = build_policy_city_year_scores_template(base)
    assert frame.loc[0, "policy_data_status"] == "pending_document_registry"
