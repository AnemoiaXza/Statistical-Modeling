from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from stat_modeling.config import POLICY_TEXT_INTERIM_DIR, POLICY_TEXT_LOGS_DIR, POLICY_TEXT_PROCESSED_DIR


def ensure_policy_text_directories() -> tuple[Path, Path, Path]:
    for directory in (POLICY_TEXT_INTERIM_DIR, POLICY_TEXT_PROCESSED_DIR, POLICY_TEXT_LOGS_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    return POLICY_TEXT_INTERIM_DIR, POLICY_TEXT_PROCESSED_DIR, POLICY_TEXT_LOGS_DIR


def _safe_suffix(source_url: str, fallback: str) -> str:
    suffix = Path(urlparse(source_url).path).suffix.lower()
    return suffix or fallback


def raw_html_path(doc_id: str) -> Path:
    ensure_policy_text_directories()
    return POLICY_TEXT_INTERIM_DIR / "raw_html" / f"{doc_id}.html"


def attachment_path(doc_id: str, source_url: str, fallback_suffix: str = ".bin") -> Path:
    ensure_policy_text_directories()
    suffix = _safe_suffix(source_url, fallback_suffix)
    return POLICY_TEXT_INTERIM_DIR / "attachments" / f"{doc_id}{suffix}"


def write_raw_html(doc_id: str, html: str) -> Path:
    destination = raw_html_path(doc_id)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8")
    return destination


def write_attachment(doc_id: str, content: bytes, source_url: str, fallback_suffix: str = ".bin") -> Path:
    destination = attachment_path(doc_id, source_url, fallback_suffix)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return destination
