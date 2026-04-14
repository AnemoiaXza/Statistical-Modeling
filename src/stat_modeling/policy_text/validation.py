from __future__ import annotations

import pandas as pd


def summarize_score_alignment(frame: pd.DataFrame) -> dict[str, dict[bool, float]]:
    summary: dict[str, dict[bool, float]] = {}
    rule_columns = [column for column in frame.columns if column.startswith("has_")]
    score_columns = [column for column in ("policy_strength", "execution_clarity", "digital_green_synergy") if column in frame.columns]

    for rule_column in rule_columns:
        grouped = frame.groupby(rule_column)[score_columns].mean(numeric_only=True)
        for score_column in score_columns:
            summary[f"{score_column}_by_{rule_column.removeprefix('has_')}"] = grouped[score_column].to_dict()
    return summary
