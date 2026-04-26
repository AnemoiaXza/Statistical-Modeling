from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.policy_text import storage


def test_write_raw_html_preserves_html_suffix(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "POLICY_TEXT_INTERIM_DIR", tmp_path / "interim")
    monkeypatch.setattr(storage, "POLICY_TEXT_PROCESSED_DIR", tmp_path / "processed")
    monkeypatch.setattr(storage, "POLICY_TEXT_LOGS_DIR", tmp_path / "logs")

    written = storage.write_raw_html("doc-1", "<html>body</html>")

    assert written.suffix == ".html"
    assert written.read_text(encoding="utf-8") == "<html>body</html>"
