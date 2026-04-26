from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.models import PolicyDocument


def test_policy_document_normalizes_required_fields():
    document = PolicyDocument(
        title="关于推进节能降碳行动的通知",
        pub_date="2024-05-29",
        issuing_body="国务院",
        admin_level="central",
        region_name="China",
        source_url="https://www.gov.cn/example",
        content_text="全文内容",
    )

    assert document.doc_id.startswith("central_2024")
    assert document.doc_no is None
