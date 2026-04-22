from __future__ import annotations

import pandas as pd


def parse_feature_columns(raw_value: str) -> list[str]:
    return [value.strip() for value in raw_value.split(",") if value.strip()]


def validate_feature_columns(frame: pd.DataFrame, feature_columns: list[str]) -> None:
    missing = [column for column in feature_columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing heterogeneity feature columns: {missing}")


def build_heterogeneity_input(
    frame: pd.DataFrame,
    treatment_column: str,
    outcome_column: str,
    feature_columns: list[str],
) -> pd.DataFrame:
    required = [treatment_column, outcome_column] + feature_columns
    filtered = frame.dropna(subset=required).copy()
    return filtered[
        [
            "year",
            "pku_city_code",
            "pku_city_name_cn",
            "pku_city_name_eng",
            treatment_column,
            outcome_column,
            *feature_columns,
        ]
    ].sort_values(["pku_city_code", "year"]).reset_index(drop=True)


def compute_feature_correlation(frame: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    return frame[feature_columns].corr().round(3)
