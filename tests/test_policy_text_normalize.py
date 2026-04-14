from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.normalize import normalize_policy_record


def test_normalize_policy_record_extracts_core_fields():
    raw_record = {
        "title": "上海市加快建立产品碳足迹管理体系行动方案",
        "pub_date": "2024-03-25",
        "issuing_body": "上海市人民政府",
        "source_url": "https://www.shanghai.gov.cn/example",
        "content_text": "提出目标、责任单位和实施期限。",
    }

    normalized = normalize_policy_record(raw_record, admin_level="municipal", region_name="上海市")

    assert normalized["admin_level"] == "municipal"
    assert normalized["region_name"] == "上海市"
    assert str(normalized["content_text"]).startswith("提出目标")
