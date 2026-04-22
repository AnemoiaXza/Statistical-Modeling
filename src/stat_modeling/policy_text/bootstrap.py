from __future__ import annotations

import pandas as pd


def build_policy_source_manifest() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "source_site": "gov.cn",
                "admin_level": "central",
                "region_name": "China",
                "base_url": "https://www.gov.cn/zhengce/zhengceku/",
                "status": "seeded",
            },
            {
                "source_site": "ndrc.gov.cn",
                "admin_level": "central",
                "region_name": "China",
                "base_url": "https://www.ndrc.gov.cn/xxgk/",
                "status": "seeded",
            },
            {
                "source_site": "mee.gov.cn",
                "admin_level": "central",
                "region_name": "China",
                "base_url": "https://www.mee.gov.cn/xxgk2018/xxgk/",
                "status": "seeded",
            },
        ]
    )


def build_policy_document_registry_template() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "doc_id",
            "title",
            "pub_date",
            "issuing_body",
            "admin_level",
            "region_name",
            "region_code",
            "doc_no",
            "source_site",
            "source_url",
            "content_text",
            "attachment_path",
            "raw_html_path",
            "is_pdf",
            "is_scanned_pdf",
            "is_official",
            "document_status",
            "has_quant_target",
            "has_deadline",
            "has_responsibility",
            "has_assessment",
            "has_digital_term",
            "policy_strength",
            "execution_clarity",
            "digital_green_synergy",
        ]
    )


def build_policy_city_year_scores_template(base_panel: pd.DataFrame) -> pd.DataFrame:
    template = base_panel[["year", "pku_city_code", "pku_city_name_cn"]].drop_duplicates().copy()
    template["policy_strength"] = pd.NA
    template["execution_clarity"] = pd.NA
    template["digital_green_synergy"] = pd.NA
    template["policy_doc_count"] = pd.NA
    template["policy_data_status"] = "pending_document_registry"
    return template.sort_values(["pku_city_code", "year"]).reset_index(drop=True)
