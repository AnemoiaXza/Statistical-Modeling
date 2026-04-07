import pandas as pd


def winsorize_series(series: pd.Series, lower: float = 0.01, upper: float = 0.99) -> pd.Series:
    lower_bound = series.quantile(lower, interpolation="higher")
    upper_bound = series.quantile(upper, interpolation="lower")
    return series.clip(lower=lower_bound, upper=upper_bound)


def interpolate_by_group(
    frame: pd.DataFrame,
    group_key: str,
    order_key: str,
    columns: list[str],
) -> pd.DataFrame:
    result = frame.sort_values([group_key, order_key]).copy()
    for column in columns:
        result[column] = result.groupby(group_key)[column].transform(
            lambda values: values.interpolate(method="linear", limit_area="inside")
        )
    return result
