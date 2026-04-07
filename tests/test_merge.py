from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.merge import assert_unique_panel_keys


def test_assert_unique_panel_keys_raises_for_duplicates():
    frame = pd.DataFrame({"city_code": [1, 1], "year": [2011, 2011]})

    with pytest.raises(ValueError):
        assert_unique_panel_keys(frame, keys=["city_code", "year"])
