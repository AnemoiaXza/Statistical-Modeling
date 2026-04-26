from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.data.yearbook_core_controls import read_yearbook_table_with_flat_headers
from stat_modeling.data.yearbook_core_controls import normalize_city_name_cn
from stat_modeling.data.yearbook_core_controls import YEARBOOK_CORE_SPECS
from stat_modeling.data.yearbook_core_controls import build_core_controls_panel


def test_read_yearbook_table_with_flat_headers_detects_data_rows(tmp_path):
    source = tmp_path / "table.xlsx"
    frame = pd.DataFrame(
        [
            ["2-7 地区生产总值", None, None],
            ["Gross Regional Product", None, None],
            ["城 市", "City", "地区生产总值(亿元)"],
            [None, None, "全 市 Total City"],
            ["北京市", "Beijing", 100],
            ["天津市", "Tianjin", 90],
        ]
    )
    frame.to_excel(source, header=False, index=False)

    result = read_yearbook_table_with_flat_headers(source)

    assert result.iloc[0, 0] == "北京市"
    assert "地区生产总值" in result.columns[2]


def test_normalize_city_name_cn_removes_whitespace():
    assert normalize_city_name_cn("  银川市 ") == "银川市"


def test_build_core_controls_panel_carries_pku_city_code(tmp_path):
    root = tmp_path / "yb"
    root.mkdir()
    specs = {}
    for key in ("gdp", "industry", "population", "fiscal"):
        path = root / f"{key}.xlsx"
        specs[key] = path.name
    pd.DataFrame(
        [
            ["title", None, None],
            ["title2", None, None],
            ["城市", "City", "地区生产总值 Total City"],
            [None, None, None],
            ["北京市", "Beijing", 100],
        ]
    ).to_excel(root / specs["gdp"], header=False, index=False)
    pd.DataFrame(
        [
            ["title", None, None],
            ["title2", None, None],
            ["城市", "City", "第二产业 Total City"],
            [None, None, None],
            ["北京市", "Beijing", 50],
        ]
    ).to_excel(root / specs["industry"], header=False, index=False)
    pd.DataFrame(
        [
            ["title", None, None],
            ["title2", None, None],
            ["城市", "City", "常住人口 Total City"],
            [None, None, None],
            ["北京市", "Beijing", 20],
        ]
    ).to_excel(root / specs["population"], header=False, index=False)
    pd.DataFrame(
        [
            ["title", None, None],
            ["title2", None, None],
            ["城市", "City", "地方一般公共预算支出 Total City"],
            [None, None, None],
            ["北京市", "Beijing", 30],
        ]
    ).to_excel(root / specs["fiscal"], header=False, index=False)

    original = YEARBOOK_CORE_SPECS.copy()
    try:
        YEARBOOK_CORE_SPECS.clear()
        YEARBOOK_CORE_SPECS[2023] = specs
        pku_ref = pd.DataFrame([{"pku_city_code": 1100, "pku_city_name_cn": "北京市", "pku_city_name_eng": "Beijing"}])
        result = build_core_controls_panel(root, pku_ref)
        assert result.loc[0, "pku_city_code"] == 1100
    finally:
        YEARBOOK_CORE_SPECS.clear()
        YEARBOOK_CORE_SPECS.update(original)
