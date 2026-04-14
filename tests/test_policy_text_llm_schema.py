from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.llm_schema import build_scoring_payload


def test_build_scoring_payload_contains_three_scores_and_document_context():
    payload = build_scoring_payload(
        title="关于加快绿色低碳转型的意见",
        content_text="明确提出责任分工、量化指标和数字平台建设要求。",
    )

    assert payload["document"]["title"] == "关于加快绿色低碳转型的意见"
    assert "policy_strength" in payload["schema"]["properties"]
    assert "execution_clarity" in payload["schema"]["properties"]
    assert "digital_green_synergy" in payload["schema"]["properties"]
