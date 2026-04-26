from __future__ import annotations

import pandas as pd


def build_modeling_candidate_panel(
    pku_cmcc_panel: pd.DataFrame,
    core_controls: pd.DataFrame,
) -> pd.DataFrame:
    controls = core_controls.copy()
    control_dup_count = int(controls.groupby(["pku_city_code", "year"]).size().gt(1).sum())
    if control_dup_count:
        raise ValueError(f"Duplicate core control keys detected: {control_dup_count}")
    pku_dup_count = int(pku_cmcc_panel.groupby(["pku_city_code", "year"]).size().gt(1).sum())
    if pku_dup_count:
        raise ValueError(f"Duplicate PKU-CMCC keys detected: {pku_dup_count}")
    merged = pku_cmcc_panel.merge(
        controls[
            [
                "pku_city_code",
                "year",
                "gdp_total",
                "secondary_industry_share",
                "population_raw",
                "fiscal_expenditure",
            ]
        ],
        on=["pku_city_code", "year"],
        how="left",
        validate="one_to_one",
    )
    merged["has_core_controls"] = merged[
        ["gdp_total", "secondary_industry_share", "population_raw", "fiscal_expenditure"]
    ].notna().all(axis=1)
    merged["ready_for_dml_candidate"] = merged["has_cmcc_outcome"] & merged["has_core_controls"]
    return merged.sort_values(["pku_city_code", "year"]).reset_index(drop=True)
