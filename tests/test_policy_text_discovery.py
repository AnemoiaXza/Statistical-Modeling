from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text.discovery import build_keyword_query, select_supported_source


def test_build_keyword_query_includes_green_and_carbon_terms():
    query = build_keyword_query(year=2024)
    assert "碳达峰" in query
    assert "数字化绿色转型" in query


def test_select_supported_source_for_gov():
    source = select_supported_source("https://www.gov.cn/zhengce")
    assert source.source_site == "gov.cn"
