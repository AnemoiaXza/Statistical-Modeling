from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.dedupe import deduplicate_policy_records


def test_deduplicate_prefers_formal_publication():
    frame = pd.DataFrame(
        [
            {"title": "通知", "pub_date": "2024-01-01", "issuing_body": "国务院", "doc_no": "国发1号", "is_official": False},
            {"title": "通知", "pub_date": "2024-01-01", "issuing_body": "国务院", "doc_no": "国发1号", "is_official": True},
        ]
    )

    result = deduplicate_policy_records(frame)

    assert len(result) == 1
    assert bool(result.iloc[0]["is_official"]) is True
