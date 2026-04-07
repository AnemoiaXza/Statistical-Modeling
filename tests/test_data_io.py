from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.io import write_table


def test_write_table_creates_parent_directory(tmp_path):
    frame = pd.DataFrame({"city_code": [110100], "year": [2011]})
    output = tmp_path / "nested" / "panel.csv"

    write_table(frame, output)

    assert output.exists()
