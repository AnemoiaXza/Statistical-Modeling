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


def expand_balanced_panel(
    frame: pd.DataFrame,
    entity_key: str,
    time_key: str,
    time_values: list[int] | None = None,
) -> pd.DataFrame:
    entities = pd.Index(frame[entity_key].dropna().unique(), name=entity_key)
    if time_values is None:
        ordered_time_values = sorted(frame[time_key].dropna().unique())
    else:
        ordered_time_values = sorted(time_values)
    times = pd.Index(ordered_time_values, name=time_key)
    index = pd.MultiIndex.from_product([entities, times])

    balanced = index.to_frame(index=False)
    return balanced.merge(frame, on=[entity_key, time_key], how="left")
