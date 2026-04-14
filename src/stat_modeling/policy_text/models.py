from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1


@dataclass(slots=True)
class PolicyDocument:
    title: str
    pub_date: str
    issuing_body: str
    admin_level: str
    region_name: str
    source_url: str
    content_text: str
    doc_no: str | None = None
    region_code: str | None = None
    source_site: str | None = None
    attachment_path: str | None = None
    raw_html_path: str | None = None
    is_pdf: bool = False
    is_scanned_pdf: bool = False
    is_official: bool = True
    document_status: str = "ready"

    @property
    def doc_id(self) -> str:
        digest = sha1(
            "|".join([self.title.strip(), self.pub_date, self.issuing_body.strip(), self.source_url]).encode("utf-8")
        ).hexdigest()[:12]
        return f"{self.admin_level}_{self.pub_date[:4]}_{digest}"

    def to_record(self) -> dict[str, object]:
        record = asdict(self)
        record["doc_id"] = self.doc_id
        return record
