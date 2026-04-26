from __future__ import annotations

from pathlib import Path

import requests

from stat_modeling.policy_text.storage import write_attachment, write_raw_html

DEFAULT_TIMEOUT = 20


def fetch_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response


def capture_html(doc_id: str, url: str, timeout: int = DEFAULT_TIMEOUT) -> Path:
    response = fetch_url(url, timeout=timeout)
    return write_raw_html(doc_id, response.text)


def capture_attachment(doc_id: str, url: str, timeout: int = DEFAULT_TIMEOUT) -> Path:
    response = fetch_url(url, timeout=timeout)
    return write_attachment(doc_id, response.content, source_url=url)
