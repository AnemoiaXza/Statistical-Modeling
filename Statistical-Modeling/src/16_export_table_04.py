from pathlib import Path

import pandas as pd

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import TABLES_DIR


SOURCE = INTERIM_DATA_DIR / "modeling" / "heterogeneity_candidate_cate.csv"
TARGET_CSV = TABLES_DIR / "table_04_heterogeneity_candidate_city_extremes.csv"
TARGET_TEX = TABLES_DIR / "table_04_heterogeneity_candidate_city_extremes.tex"


def main() -> int:
    frame = pd.read_csv(SOURCE)
    city = (
        frame.groupby(["pku_city_code", "pku_city_name_cn", "pku_city_name_eng"], as_index=False)
        .agg(
            cate_mean=("cate_hat", "mean"),
            cate_ci_lower_mean=("cate_ci_lower", "mean"),
            cate_ci_upper_mean=("cate_ci_upper", "mean"),
        )
        .sort_values("cate_mean")
        .reset_index(drop=True)
    )

    bottom = city.head(5).copy()
    bottom["组别"] = "Bottom 5"
    top = city.tail(5).sort_values("cate_mean", ascending=False).copy()
    top["组别"] = "Top 5"
    display = pd.concat([bottom, top], ignore_index=True)[
        ["组别", "pku_city_name_cn", "cate_mean", "cate_ci_lower_mean", "cate_ci_upper_mean"]
    ].copy()
    display.columns = ["组别", "城市", "平均CATE", "平均CI下限", "平均CI上限"]
    for column in ["平均CATE", "平均CI下限", "平均CI上限"]:
        display[column] = display[column].map(lambda x: f"{x:.4f}")

    display.to_csv(TARGET_CSV, index=False)
    latex = display.to_latex(
        index=False,
        escape=False,
        caption="候选异质性技术结果：城市平均 CATE 极值（非最终 headline 结果）",
        label="tab:heterogeneity_candidate_extremes",
    )
    TARGET_TEX.write_text(latex, encoding="utf-8")
    print(f"CSV table written to: {TARGET_CSV}")
    print(f"LaTeX table written to: {TARGET_TEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
