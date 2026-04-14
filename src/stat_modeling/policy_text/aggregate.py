from __future__ import annotations

import pandas as pd

SCORE_COLUMNS = ("policy_strength", "execution_clarity", "digital_green_synergy")


def _with_year(frame: pd.DataFrame) -> pd.DataFrame:
    if "year" in frame.columns:
        return frame.copy()
    result = frame.copy()
    result["year"] = pd.to_datetime(result["pub_date"], errors="coerce").dt.year
    return result


def assign_documents_to_cities(documents: pd.DataFrame, cities: pd.DataFrame) -> pd.DataFrame:
    documents_with_year = _with_year(documents)
    city_panel = cities.copy()

    central = documents_with_year.loc[documents_with_year["admin_level"] == "central"].merge(city_panel, on="year", how="inner")
    provincial = documents_with_year.loc[documents_with_year["admin_level"] == "provincial"].merge(
        city_panel,
        left_on=["region_name", "year"],
        right_on=["province_name_cn", "year"],
        how="inner",
    )
    municipal = documents_with_year.loc[documents_with_year["admin_level"] == "municipal"].merge(
        city_panel,
        left_on=["region_name", "year"],
        right_on=["city_name_cn", "year"],
        how="inner",
    )

    frames = [frame for frame in (central, provincial, municipal) if not frame.empty]
    if not frames:
        return pd.DataFrame(columns=[*documents_with_year.columns, *city_panel.columns])
    return pd.concat(frames, ignore_index=True)


def aggregate_policy_scores(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(
            columns=[
                "city_name_cn",
                "province_name_cn",
                "year",
                "sum_policy_strength_city_year",
                "mean_policy_strength_city_year",
                "sum_execution_clarity_city_year",
                "mean_execution_clarity_city_year",
                "sum_digital_green_synergy_city_year",
                "mean_digital_green_synergy_city_year",
            ]
        )

    aggregations: dict[str, tuple[str, str]] = {}
    for score_column in SCORE_COLUMNS:
        aggregations[f"sum_{score_column}_city_year"] = (score_column, "sum")
        aggregations[f"mean_{score_column}_city_year"] = (score_column, "mean")

    return frame.groupby(["city_name_cn", "province_name_cn", "year"], as_index=False).agg(**aggregations)
