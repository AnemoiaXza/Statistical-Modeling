from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling import config


def test_policy_text_directories_are_registered():
    expected_directories = (
        config.POLICY_TEXT_INTERIM_DIR,
        config.POLICY_TEXT_PROCESSED_DIR,
        config.POLICY_TEXT_LOGS_DIR,
    )

    assert config.POLICY_TEXT_INTERIM_DIR == config.INTERIM_DATA_DIR / "policy_text"
    assert config.POLICY_TEXT_PROCESSED_DIR == config.PROCESSED_DATA_DIR / "policy_text"
    assert config.POLICY_TEXT_LOGS_DIR == config.LOGS_DIR / "policy_text"
    assert all(path in config.REQUIRED_DIRECTORIES for path in expected_directories)


def test_ensure_project_directories_creates_policy_text_directories(tmp_path, monkeypatch):
    policy_directories = (
        tmp_path / "interim" / "policy_text",
        tmp_path / "processed" / "policy_text",
        tmp_path / "logs" / "policy_text",
    )

    monkeypatch.setattr(config, "POLICY_TEXT_INTERIM_DIR", policy_directories[0])
    monkeypatch.setattr(config, "POLICY_TEXT_PROCESSED_DIR", policy_directories[1])
    monkeypatch.setattr(config, "POLICY_TEXT_LOGS_DIR", policy_directories[2])
    monkeypatch.setattr(config, "REQUIRED_DIRECTORIES", policy_directories)

    created = config.ensure_project_directories()

    assert created == list(policy_directories)
    assert all(path.exists() for path in policy_directories)
