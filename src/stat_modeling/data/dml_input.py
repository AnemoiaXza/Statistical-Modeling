from __future__ import annotations

import numpy as np
import pandas as pd


def build_dml_candidate_input(panel: pd.DataFrame) -> pd.DataFrame:
    working = panel.loc[panel["ready_for_dml_candidate"]].copy()
    working["co2_emission_intensity"] = np.where(
        working["gdp_total"] > 0,
        working["co2_emission_total"] / working["gdp_total"],
        np.nan,
    )
    working["population_control_candidate"] = working["population_raw"]
    return working[
        [
            "year",
            "pku_city_code",
            "pku_city_name_cn",
            "pku_city_name_eng",
            "digital_inclusive_finance_index",
            "dfi_coverage_breadth",
            "dfi_usage_depth",
            "dfi_digitization_level",
            "co2_emission_total",
            "co2_emission_intensity",
            "gdp_total",
            "secondary_industry_share",
            "population_control_candidate",
            "fiscal_expenditure",
            "match_status",
        ]
    ].sort_values(["pku_city_code", "year"]).reset_index(drop=True)
