from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

KEY_TERMS = (
    "双碳",
    "碳达峰",
    "碳中和",
    "节能降碳",
    "绿色低碳",
    "数字绿色融合",
    "数字化绿色转型",
)


@dataclass(frozen=True, slots=True)
class SupportedSource:
    source_site: str
    url_patterns: tuple[str, ...]


SUPPORTED_SOURCES = (
    SupportedSource("gov.cn", ("gov.cn",)),
    SupportedSource("ndrc.gov.cn", ("ndrc.gov.cn",)),
    SupportedSource("mee.gov.cn", ("mee.gov.cn",)),
    SupportedSource("provincial.gov.cn", (".gov.cn",)),
)


def build_keyword_query(year: int) -> str:
    return f"{year} " + " OR ".join(KEY_TERMS)


def select_supported_source(url: str) -> SupportedSource:
    hostname = urlparse(url).netloc.lower()
    for source in SUPPORTED_SOURCES:
        for pattern in source.url_patterns:
            if pattern.startswith(".") and hostname.endswith(pattern):
                return source
            if hostname == pattern or hostname.endswith(f".{pattern}"):
                return source
    raise ValueError(f"Unsupported policy source: {url}")
