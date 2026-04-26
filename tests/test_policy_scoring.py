from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.scoring import score_policy_rule_proxy


def test_score_policy_rule_proxy_assigns_numeric_scores():
    frame = pd.DataFrame(
        [
            {
                "content_text": "到2025年推进节能降碳，由有关部门负责并开展考核。",
                "has_quant_target": True,
                "has_deadline": True,
                "has_responsibility": True,
                "has_assessment": True,
                "has_digital_term": False,
            }
        ]
    )
    result = score_policy_rule_proxy(frame)
    assert float(result.loc[0, "policy_strength"]) > 1.0
    assert float(result.loc[0, "execution_clarity"]) > 1.0
    assert float(result.loc[0, "digital_green_synergy"]) > 1.0
