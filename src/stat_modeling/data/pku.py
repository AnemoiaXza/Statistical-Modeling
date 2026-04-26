from __future__ import annotations

from pathlib import Path

import pandas as pd


PKU_PREFECTURE_COLUMNS = [
    "year",
    "pref_name_year18",
    "pref_name_year18_eng",
    "pref_code_year18",
    "index_aggregate",
    "coverage_breadth",
    "usage_depth",
    "payment",
    "insurance",
    "monetary_fund",
    "investment",
    "credit",
    "credit_investigation",
    "digitization_level",
]

PKU_ENGLISH_NAME_OVERRIDES = {
    1306: "Baoding",
    6103: "Baoji",
    3205: "Suzhou",
    3413: "Suzhou_anhui",
    3310: "Taizhou",
    3212: "Taizhou_jiangsu",
    3501: "Fuzhou",
    3610: "Fuzhou_jiangxi",
    3609: "Yichun",
    2307: "Yichun_heilongjiang",
    4509: "Yulin",
    6108: "Yulin_shanxi",
    4114: "Shangqiu",
    4402: "Shaoguan",
    4409: "Maoming",
    4603: "Sansha",
    4604: "Danzhou",
    5132: "Aba",
    6501: "Urumqi",
    1522: "Xing'an",
    6528: "Bayin'gholin Mongol",
    1508: "Baynnur",
    5403: "Chamdo",
    5334: "Dêqên Tibetan",
    5133: "Garzê Tibetan",
    6326: "Golog Tibetan",
    6327: "Gyêgu Tibetan",
    5325: "Honghe Hani and Yi",
    6540: "Ili Kazakh",
    6531: "Kashgar",
    6530: "Kizilsu Kirghiz",
    5404: "Nyingtri",
    5226: "Qiandongnan Miao and Dong",
    5328: "Xishuangbanna Dai",
    5326: "Wenshan Zhuang and Miao",
}


def load_pku_prefecture_panel(
    pku_path: str | Path,
    year_min: int | None = None,
    year_max: int | None = None,
) -> pd.DataFrame:
    frame = pd.read_excel(
        pku_path,
        sheet_name="Prefecture_Level_Cities",
        usecols=PKU_PREFECTURE_COLUMNS,
    ).copy()

    frame = frame.rename(
        columns={
            "pref_name_year18": "pku_city_name_cn",
            "pref_name_year18_eng": "pku_city_name_eng_raw",
            "pref_code_year18": "pku_city_code",
            "index_aggregate": "digital_inclusive_finance_index",
            "coverage_breadth": "dfi_coverage_breadth",
            "usage_depth": "dfi_usage_depth",
            "digitization_level": "dfi_digitization_level",
        }
    )

    if year_min is not None:
        frame = frame.loc[frame["year"] >= year_min]
    if year_max is not None:
        frame = frame.loc[frame["year"] <= year_max]

    frame["pku_city_code"] = frame["pku_city_code"].astype(int)
    frame["pku_city_name_eng"] = frame["pku_city_code"].map(PKU_ENGLISH_NAME_OVERRIDES).fillna(
        frame["pku_city_name_eng_raw"].astype(str).str.strip()
    )
    frame = frame.sort_values(["pku_city_code", "year"]).reset_index(drop=True)
    return frame


def build_pku_cmcc_candidate_panel(
    pku_panel: pd.DataFrame,
    cmcc_resolved_panel: pd.DataFrame,
    year_min: int = 2019,
    year_max: int = 2023,
) -> pd.DataFrame:
    pku_filtered = pku_panel.loc[(pku_panel["year"] >= year_min) & (pku_panel["year"] <= year_max)].copy()
    cmcc_filtered = cmcc_resolved_panel.loc[
        (cmcc_resolved_panel["year"] >= year_min) & (cmcc_resolved_panel["year"] <= year_max)
    ].copy()
    cmcc_filtered["pku_city_code"] = cmcc_filtered["pku_city_code"].astype(int)

    merged = pku_filtered.merge(
        cmcc_filtered[
            [
                "pku_city_code",
                "year",
                "annual_total_value",
                "match_status",
                "city",
                "pku_city_name_cn",
            ]
        ].rename(
            columns={
                "annual_total_value": "co2_emission_total",
                "city": "cmcc_city_name_raw",
                "pku_city_name_cn": "cmcc_mapped_city_name_cn",
            }
        ),
        on=["pku_city_code", "year"],
        how="left",
    )
    merged["has_cmcc_outcome"] = merged["co2_emission_total"].notna()
    return merged.sort_values(["pku_city_code", "year"]).reset_index(drop=True)
