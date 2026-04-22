from pathlib import Path

import pandas as pd

from stat_modeling.config import TABLES_DIR


SOURCE = TABLES_DIR / "table_02_dml_main_and_robustness.csv"
TARGET = TABLES_DIR / "table_02_dml_main_and_robustness.tex"


def main() -> int:
    frame = pd.read_csv(SOURCE)
    display = frame[
        [
            "outcome_label_cn",
            "ate",
            "std_error",
            "ci_lower",
            "ci_upper",
            "p_value",
            "nobs",
        ]
    ].copy()
    display.columns = [
        "结果变量",
        "ATE",
        "标准误",
        "95%CI下限",
        "95%CI上限",
        "P值",
        "样本量",
    ]
    for column in ["ATE", "标准误", "95%CI下限", "95%CI上限", "P值"]:
        display[column] = display[column].map(lambda x: f"{x:.4f}")
    display["样本量"] = display["样本量"].astype(int).astype(str)
    latex = display.to_latex(index=False, escape=False, caption="DML主结果与稳健性结果", label="tab:dml_main")
    TARGET.write_text(latex, encoding="utf-8")
    print(f"LaTeX table written to: {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
