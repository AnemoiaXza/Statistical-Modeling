from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.validation import summarize_score_alignment


def test_summarize_score_alignment_reports_rule_llm_directions():
    frame = pd.DataFrame(
        [
            {"has_quant_target": True, "policy_strength": 4.5},
            {"has_quant_target": False, "policy_strength": 1.0},
        ]
    )

    summary = summarize_score_alignment(frame)

    assert "policy_strength_by_quant_target" in summary
    assert summary["policy_strength_by_quant_target"][True] > summary["policy_strength_by_quant_target"][False]
