from __future__ import annotations

import pandas as pd


def merge_modeling_with_policy_seed(
    modeling_panel: pd.DataFrame,
    policy_seed_panel: pd.DataFrame,
) -> pd.DataFrame:
    return modeling_panel.merge(
        policy_seed_panel,
        on=["year", "pku_city_code", "pku_city_name_cn"],
        how="left",
        validate="one_to_one",
    )
