from collections.abc import Iterable

import pandas as pd


def assert_unique_panel_keys(frame: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    duplicated = frame.duplicated(subset=keys, keep=False)
    if duplicated.any():
        duplicate_rows = frame.loc[duplicated, keys].drop_duplicates().to_dict(orient="records")
        raise ValueError(f"Duplicate panel keys detected: {duplicate_rows}")
    return frame


def merge_source_tables(
    base_frame: pd.DataFrame,
    other_frames: Iterable[pd.DataFrame],
    keys: list[str],
    how: str = "left",
) -> pd.DataFrame:
    result = base_frame.copy()
    for frame in other_frames:
        result = result.merge(frame, on=keys, how=how)
    return result


def summarize_cleaning(frame: pd.DataFrame) -> pd.DataFrame:
    summary = pd.DataFrame(
        {
            "column": frame.columns,
            "missing_count": [int(frame[column].isna().sum()) for column in frame.columns],
            "missing_rate": [float(frame[column].isna().mean()) for column in frame.columns],
        }
    )
    summary.attrs["row_count"] = int(len(frame))
    summary.attrs["column_count"] = int(frame.shape[1])
    return summary
