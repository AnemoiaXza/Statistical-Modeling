from __future__ import annotations

import pandas as pd


def score_policy_rule_proxy(frame: pd.DataFrame) -> pd.DataFrame:
    scored = frame.copy()
    for column in ["has_quant_target", "has_deadline", "has_responsibility", "has_assessment", "has_digital_term"]:
        if column not in scored.columns:
            scored[column] = False

    scored["policy_strength"] = (
        1.0
        + scored["has_quant_target"].astype(int) * 1.5
        + scored["has_deadline"].astype(int) * 1.0
        + scored["has_assessment"].astype(int) * 0.5
    )
    scored["execution_clarity"] = (
        1.0
        + scored["has_responsibility"].astype(int) * 1.5
        + scored["has_deadline"].astype(int) * 1.0
        + scored["has_assessment"].astype(int) * 1.0
    )
    scored["digital_green_synergy"] = (
        1.0
        + scored["has_digital_term"].astype(int) * 2.0
        + scored["content_text"].astype(str).str.contains("节能|降碳|碳达峰|碳中和", regex=True).astype(int) * 1.0
    )
    scored["score_method"] = "seed_rule_proxy"
    return scored
