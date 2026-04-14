from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.config import ensure_project_directories


def test_policy_text_directories_are_created(tmp_path, monkeypatch):
    monkeypatch.setattr("stat_modeling.config.INTERIM_DATA_DIR", tmp_path / "interim")
    monkeypatch.setattr("stat_modeling.config.PROCESSED_DATA_DIR", tmp_path / "processed")
    monkeypatch.setattr("stat_modeling.config.LOGS_DIR", tmp_path / "logs")

    created = ensure_project_directories()

    assert any(path.name == "policy_text" for path in created)
    assert (tmp_path / "interim" / "policy_text").exists()
    assert (tmp_path / "processed" / "policy_text").exists()
    assert (tmp_path / "logs" / "policy_text").exists()
