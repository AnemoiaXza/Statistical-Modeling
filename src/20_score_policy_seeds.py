import argparse
from pathlib import Path
from typing import Sequence

import pandas as pd

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text
from stat_modeling.policy_text.aggregate import aggregate_policy_scores
from stat_modeling.policy_text.aggregate import assign_documents_to_cities
from stat_modeling.policy_text.scoring import score_policy_rule_proxy


DEFAULT_REGISTRY = INTERIM_DATA_DIR / "policy_text" / "policy_document_registry_seed_central.csv"
DEFAULT_CITY_YEAR_TEMPLATE = INTERIM_DATA_DIR / "policy_text" / "policy_city_year_scores_template.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score seeded policy documents with a transparent rule proxy and aggregate to city-year.")
    parser.add_argument("--registry-path", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--city-year-template-path", type=Path, default=DEFAULT_CITY_YEAR_TEMPLATE)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_project_directories()

    registry = read_table(args.registry_path)
    city_year_template = read_table(args.city_year_template_path)

    scored = score_policy_rule_proxy(registry)
    scored_path = INTERIM_DATA_DIR / "policy_text" / "policy_document_registry_seed_scored.csv"
    write_table(scored, scored_path)

    city_panel = city_year_template.rename(columns={"pku_city_name_cn": "city_name_cn"}).copy()
    city_panel["province_name_cn"] = None
    assigned = assign_documents_to_cities(scored, city_panel[["city_name_cn", "province_name_cn", "year"]])

    aggregated_path = INTERIM_DATA_DIR / "policy_text" / "policy_city_year_scores_seed_scored.csv"
    if assigned.empty:
        aggregated_template = city_year_template.copy()
        aggregated_template["sum_policy_strength_city_year"] = pd.NA
        aggregated_template["mean_policy_strength_city_year"] = pd.NA
        aggregated_template["sum_execution_clarity_city_year"] = pd.NA
        aggregated_template["mean_execution_clarity_city_year"] = pd.NA
        aggregated_template["sum_digital_green_synergy_city_year"] = pd.NA
        aggregated_template["mean_digital_green_synergy_city_year"] = pd.NA
        aggregated_template["policy_doc_count"] = 0
        write_table(aggregated_template, aggregated_path)
        aggregated = aggregated_template
    else:
        aggregated = aggregate_policy_scores(assigned)
        counts = assigned.groupby(["city_name_cn", "year"], as_index=False).size().rename(columns={"size": "policy_doc_count"})
        aggregated = aggregated.merge(counts, on=["city_name_cn", "year"], how="left", validate="one_to_one")
        base_template = city_year_template.drop(
            columns=[
                "policy_strength",
                "execution_clarity",
                "digital_green_synergy",
                "policy_doc_count",
                "policy_data_status",
            ],
            errors="ignore",
        )
        aggregated = base_template.merge(
            aggregated,
            left_on=["pku_city_name_cn", "year"],
            right_on=["city_name_cn", "year"],
            how="left",
            validate="one_to_one",
        ).drop(columns=["city_name_cn", "province_name_cn"])
        aggregated["policy_data_status"] = "seed_rule_proxy_scored"
        aggregated["policy_doc_count"] = aggregated["policy_doc_count"].fillna(0).astype(int)
        write_table(aggregated, aggregated_path)

    summary = "\n".join(
        [
            "Policy Seed Scoring Summary",
            f"scored_registry: {scored_path}",
            f"aggregated_scores: {aggregated_path}",
            f"registry_docs: {len(scored)}",
            f"aggregated_rows: {len(aggregated)}",
            "boundary_note: these are transparent rule-proxy scores for seeded central documents, not final validated LLM scores.",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / "policy_seed_scoring_summary.txt")
    print(f"Seed scored registry written to: {scored_path}")
    print(f"Seed aggregated scores written to: {aggregated_path}")
    print(f"Summary written to: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
