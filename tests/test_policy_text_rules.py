from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.rules import extract_rule_features


def test_extract_rule_features_detects_targets_deadlines_and_digital_terms():
    text = "到2025年实现单位能耗下降3%，由市发展改革委牵头，建立年度考核机制，推进数字化绿色转型。"

    features = extract_rule_features(text)

    assert features["has_quant_target"] is True
    assert features["has_deadline"] is True
    assert features["has_responsibility"] is True
    assert features["has_assessment"] is True
    assert features["has_digital_term"] is True
