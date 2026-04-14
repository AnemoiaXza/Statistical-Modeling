from __future__ import annotations

import pandas as pd


def _build_dedupe_key(frame: pd.DataFrame) -> pd.Series:
    doc_numbers = frame.get("doc_no", pd.Series(index=frame.index, dtype="object")).fillna("").astype(str).str.strip()
    title = frame.get("title", pd.Series(index=frame.index, dtype="object")).fillna("").astype(str).str.strip()
    pub_date = frame.get("pub_date", pd.Series(index=frame.index, dtype="object")).fillna("").astype(str).str.strip()
    issuing_body = frame.get("issuing_body", pd.Series(index=frame.index, dtype="object")).fillna("").astype(str).str.strip()
    title_keys = title + "|" + pub_date + "|" + issuing_body
    return doc_numbers.where(doc_numbers != "", title_keys)


def deduplicate_policy_records(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame.copy()

    dedupe_key = _build_dedupe_key(frame)
    ordered = (
        frame.assign(_dedupe_key=dedupe_key, _is_official=frame.get("is_official", False).astype(bool))
        .sort_values(["_dedupe_key", "_is_official"], ascending=[True, False])
        .drop_duplicates(subset=["_dedupe_key"], keep="first")
        .drop(columns=["_dedupe_key", "_is_official"])
        .reset_index(drop=True)
    )
    return ordered
