from __future__ import annotations

from urllib.parse import urlparse

from stat_modeling.policy_text.models import PolicyDocument


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def normalize_policy_record(raw_record: dict[str, object], admin_level: str, region_name: str) -> dict[str, object]:
    document = PolicyDocument(
        title=normalize_whitespace(str(raw_record["title"])),
        pub_date=str(raw_record["pub_date"]),
        issuing_body=normalize_whitespace(str(raw_record["issuing_body"])),
        admin_level=admin_level,
        region_name=region_name,
        region_code=str(raw_record["region_code"]) if raw_record.get("region_code") else None,
        source_url=str(raw_record["source_url"]),
        source_site=str(raw_record.get("source_site") or urlparse(str(raw_record["source_url"])).netloc.lower()),
        content_text=normalize_whitespace(str(raw_record["content_text"])),
        doc_no=normalize_whitespace(str(raw_record["doc_no"])) if raw_record.get("doc_no") else None,
        attachment_path=str(raw_record["attachment_path"]) if raw_record.get("attachment_path") else None,
        raw_html_path=str(raw_record["raw_html_path"]) if raw_record.get("raw_html_path") else None,
        is_pdf=bool(raw_record.get("is_pdf", False)),
        is_scanned_pdf=bool(raw_record.get("is_scanned_pdf", False)),
        is_official=bool(raw_record.get("is_official", True)),
        document_status=str(raw_record.get("document_status") or ("ocr_pending" if raw_record.get("is_scanned_pdf") else "ready")),
    )
    return document.to_record()
