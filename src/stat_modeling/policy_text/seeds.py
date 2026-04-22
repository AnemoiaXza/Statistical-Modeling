from __future__ import annotations

import pandas as pd

from stat_modeling.policy_text.aggregate import assign_documents_to_cities
from stat_modeling.policy_text.models import PolicyDocument
from stat_modeling.policy_text.normalize import normalize_policy_record
from stat_modeling.policy_text.rules import extract_rule_features


def build_central_policy_seed_records() -> list[dict[str, object]]:
    seeds = [
        {
            "title": "中共中央 国务院关于完整准确全面贯彻新发展理念做好碳达峰碳中和工作的意见",
            "pub_date": "2021-10-24",
            "issuing_body": "中共中央 国务院",
            "admin_level": "central",
            "region_name": "China",
            "source_url": "https://www.gov.cn/zhengce/2021-10/24/content_5644613.htm",
            "source_site": "gov.cn",
            "content_text": "完整准确全面贯彻新发展理念，做好碳达峰碳中和工作，提出到2025年、2030年、2060年的阶段目标，强调责任落实、监督考核和统筹推进。",
            "doc_no": None,
        },
        {
            "title": "国务院关于印发2030年前碳达峰行动方案的通知",
            "pub_date": "2021-10-26",
            "issuing_body": "国务院",
            "admin_level": "central",
            "region_name": "China",
            "source_url": "https://www.gov.cn/zhengce/content/2021-10/26/content_5644984.htm",
            "source_site": "gov.cn",
            "content_text": "印发2030年前碳达峰行动方案，提出节能降碳增效、工业领域碳达峰、城乡建设碳达峰等重点行动，包含时间节点、重点工程和政策要求。",
            "doc_no": None,
        },
        {
            "title": "国务院印发《2024—2025年节能降碳行动方案》",
            "pub_date": "2024-05-29",
            "issuing_body": "国务院",
            "admin_level": "central",
            "region_name": "China",
            "source_url": "https://www.gov.cn/zhengce/zhengceku/202405/content_6954321.htm",
            "source_site": "gov.cn",
            "content_text": "部署2024—2025年节能降碳行动，提出单位能耗、二氧化碳排放强度和重点行业节能降碳目标，强调重点任务、责任部门和年度推进安排。",
            "doc_no": None,
        },
    ]
    normalized_records = []
    for raw in seeds:
        record = normalize_policy_record(raw, admin_level=raw["admin_level"], region_name=raw["region_name"])
        record.update(extract_rule_features(record["content_text"]))
        normalized_records.append(record)
    return normalized_records


def build_seed_registry_frame() -> pd.DataFrame:
    return pd.DataFrame(build_central_policy_seed_records())


def build_seed_city_year_doc_counts(
    registry_frame: pd.DataFrame,
    city_year_template: pd.DataFrame,
) -> pd.DataFrame:
    city_panel = city_year_template[["year", "pku_city_code", "pku_city_name_cn"]].copy()
    city_panel["city_name_cn"] = city_panel["pku_city_name_cn"]
    city_panel["province_name_cn"] = None
    assigned = assign_documents_to_cities(registry_frame, city_panel[["city_name_cn", "province_name_cn", "year"]])
    if assigned.empty:
        result = city_year_template.copy()
        result["policy_doc_count_seeded"] = 0
        return result

    counts = (
        assigned.groupby(["city_name_cn", "year"], as_index=False)
        .size()
        .rename(columns={"size": "policy_doc_count_seeded"})
    )
    result = city_year_template.merge(
        counts,
        left_on=["pku_city_name_cn", "year"],
        right_on=["city_name_cn", "year"],
        how="left",
    ).drop(columns=["city_name_cn"])
    result["policy_doc_count_seeded"] = result["policy_doc_count_seeded"].fillna(0).astype(int)
    return result
