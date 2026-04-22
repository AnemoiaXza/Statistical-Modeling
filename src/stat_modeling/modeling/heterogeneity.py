from __future__ import annotations

from dataclasses import dataclass

import numpy as np
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


@dataclass(slots=True)
class HeterogeneityResult:
    nobs: int
    cate_mean: float
    cate_std: float
    cate_min: float
    cate_q25: float
    cate_median: float
    cate_q75: float
    cate_max: float
    feature_columns: str
    control_columns: str
    treatment_column: str
    outcome_column: str

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "nobs": self.nobs,
                    "cate_mean": self.cate_mean,
                    "cate_std": self.cate_std,
                    "cate_min": self.cate_min,
                    "cate_q25": self.cate_q25,
                    "cate_median": self.cate_median,
                    "cate_q75": self.cate_q75,
                    "cate_max": self.cate_max,
                    "feature_columns": self.feature_columns,
                    "control_columns": self.control_columns,
                    "treatment_column": self.treatment_column,
                    "outcome_column": self.outcome_column,
                }
            ]
        )


def fit_candidate_cate(
    frame: pd.DataFrame,
    treatment_column: str,
    outcome_column: str,
    feature_columns: list[str],
    control_columns: list[str],
    random_seed: int = 42,
):
    from econml.dml import CausalForestDML
    from sklearn.ensemble import GradientBoostingRegressor

    required = [treatment_column, outcome_column] + feature_columns + control_columns
    filtered = frame.dropna(subset=list(dict.fromkeys(required))).reset_index(drop=True)

    x = filtered[feature_columns].to_numpy(dtype=float)
    w = filtered[control_columns].to_numpy(dtype=float) if control_columns else None
    t = filtered[treatment_column].to_numpy(dtype=float)
    y = filtered[outcome_column].to_numpy(dtype=float)

    est = CausalForestDML(
        model_y=GradientBoostingRegressor(random_state=random_seed),
        model_t=GradientBoostingRegressor(random_state=random_seed),
        n_estimators=400,
        min_samples_leaf=10,
        max_depth=None,
        cv=3,
        random_state=random_seed,
    )
    est.fit(y, t, X=x, W=w)
    cate = np.asarray(est.effect(X=x), dtype=float)
    interval_low, interval_high = est.effect_interval(X=x)

    result = HeterogeneityResult(
        nobs=int(len(filtered)),
        cate_mean=float(np.mean(cate)),
        cate_std=float(np.std(cate)),
        cate_min=float(np.min(cate)),
        cate_q25=float(np.quantile(cate, 0.25)),
        cate_median=float(np.quantile(cate, 0.50)),
        cate_q75=float(np.quantile(cate, 0.75)),
        cate_max=float(np.max(cate)),
        feature_columns=", ".join(feature_columns),
        control_columns=", ".join(control_columns),
        treatment_column=treatment_column,
        outcome_column=outcome_column,
    )
    output = filtered[["year", "pku_city_code", "pku_city_name_cn", "pku_city_name_eng"]].copy()
    output["cate_hat"] = cate
    output["cate_ci_lower"] = np.asarray(interval_low, dtype=float)
    output["cate_ci_upper"] = np.asarray(interval_high, dtype=float)
    return output, result
