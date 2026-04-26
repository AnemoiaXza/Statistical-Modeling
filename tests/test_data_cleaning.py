from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.cleaning import interpolate_by_group, winsorize_series


def test_winsorize_series_caps_extreme_values():
    values = pd.Series([1, 2, 3, 100])

    result = winsorize_series(values, lower=0.0, upper=0.75)

    assert result.max() == 3


def test_interpolate_by_group_fills_internal_missing_values():
    frame = pd.DataFrame(
        {"city_code": [1, 1, 1], "year": [2011, 2012, 2013], "value": [1.0, None, 3.0]}
    )

    result = interpolate_by_group(frame, group_key="city_code", order_key="year", columns=["value"])

    assert result.loc[result["year"] == 2012, "value"].iat[0] == 2.0
