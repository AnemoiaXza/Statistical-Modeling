from __future__ import annotations


def extract_rule_features(text: str) -> dict[str, bool | int]:
    normalized = text.replace("\n", " ")
    features = {
        "has_quant_target": any(token in normalized for token in ("%", "目标", "下降", "提升", "减少")),
        "has_deadline": any(token in normalized for token in ("到202", "期限", "年底前", "年度")),
        "has_responsibility": any(token in normalized for token in ("负责", "牵头", "责任单位", "部门")),
        "has_assessment": any(token in normalized for token in ("考核", "问责", "监督", "评估")),
        "has_digital_term": any(token in normalized for token in ("数字", "数据", "智能", "平台")),
    }
    features["policy_level"] = sum(bool(value) for value in features.values())
    return features
