from pathlib import Path

import pandas as pd

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import TABLES_DIR


SOURCE = INTERIM_DATA_DIR / "modeling" / "heterogeneity_candidate_cate_summary.csv"
TARGET_CSV = TABLES_DIR / "table_03_heterogeneity_candidate_summary.csv"
TARGET_TEX = TABLES_DIR / "table_03_heterogeneity_candidate_summary.tex"


def main() -> int:
    frame = pd.read_csv(SOURCE)
    display = frame[
        [
            "nobs",
            "cate_mean",
            "cate_std",
            "cate_q25",
            "cate_median",
            "cate_q75",
            "feature_columns",
        ]
    ].copy()
    display.columns = [
        "样本量",
        "CATE均值",
        "CATE标准差",
        "CATE 25%分位",
        "CATE中位数",
        "CATE 75%分位",
        "候选特征集",
    ]
    for column in ["CATE均值", "CATE标准差", "CATE 25%分位", "CATE中位数", "CATE 75%分位"]:
        display[column] = display[column].map(lambda x: f"{x:.4f}")
    display["样本量"] = display["样本量"].astype(int).astype(str)
    display.to_csv(TARGET_CSV, index=False)
    latex = display.to_latex(
        index=False,
        escape=False,
        caption="候选异质性技术结果摘要（非最终 headline 结果）",
        label="tab:heterogeneity_candidate",
    )
    TARGET_TEX.write_text(latex, encoding="utf-8")
    print(f"CSV table written to: {TARGET_CSV}")
    print(f"LaTeX table written to: {TARGET_TEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
