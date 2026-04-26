from __future__ import annotations

import pandas as pd


def build_policy_mechanism_template(base_panel: pd.DataFrame) -> pd.DataFrame:
    template = base_panel[["year", "pku_city_code", "pku_city_name_cn"]].drop_duplicates().copy()
    template["policy_strength"] = pd.NA
    template["execution_clarity"] = pd.NA
    template["digital_green_synergy"] = pd.NA
    template["policy_doc_count"] = pd.NA
    template["mechanism_data_status"] = "pending_policy_text_ingest"
    return template.sort_values(["pku_city_code", "year"]).reset_index(drop=True)


def merge_policy_mechanism(
    base_panel: pd.DataFrame,
    mechanism_panel: pd.DataFrame,
) -> pd.DataFrame:
    return base_panel.merge(
        mechanism_panel,
        on=["pku_city_code", "pku_city_name_cn", "year"],
        how="left",
        validate="one_to_one",
    )
