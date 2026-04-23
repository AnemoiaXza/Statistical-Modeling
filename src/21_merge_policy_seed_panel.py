import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text


DEFAULT_TEMPLATE = INTERIM_DATA_DIR / "policy_text" / "policy_mechanism_template_2019_2023.csv"
DEFAULT_SCORES = INTERIM_DATA_DIR / "policy_text" / "policy_city_year_scores_seed_scored.csv"
DEFAULT_OUTPUT = INTERIM_DATA_DIR / "policy_text" / "policy_mechanism_seed_panel_2019_2023.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge seeded policy scores into the mechanism template.")
    parser.add_argument("--template-path", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--scores-path", type=Path, default=DEFAULT_SCORES)
    parser.add_argument("--output-path", type=Path, default=DEFAULT_OUTPUT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_project_directories()
    template = read_table(args.template_path)
    scores = read_table(args.scores_path)
    merged = template.drop(
        columns=["policy_strength", "execution_clarity", "digital_green_synergy", "policy_doc_count", "mechanism_data_status"],
        errors="ignore",
    ).merge(
        scores[
            [
                "year",
                "pku_city_code",
                "pku_city_name_cn",
                "sum_policy_strength_city_year",
                "mean_policy_strength_city_year",
                "sum_execution_clarity_city_year",
                "mean_execution_clarity_city_year",
                "sum_digital_green_synergy_city_year",
                "mean_digital_green_synergy_city_year",
                "policy_doc_count",
                "policy_data_status",
            ]
        ],
        on=["year", "pku_city_code", "pku_city_name_cn"],
        how="left",
        validate="one_to_one",
    )
    write_table(merged, args.output_path)
    summary = "\n".join(
        [
            "Policy Mechanism Seed Panel Summary",
            f"output_path: {args.output_path}",
            f"rows: {len(merged)}",
            f"city_count: {merged['pku_city_code'].nunique()}",
            f"nonzero_doc_rows: {int((merged['policy_doc_count'].fillna(0) > 0).sum())}",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / "policy_mechanism_seed_panel_summary.txt")
    print(f"Seed mechanism panel written to: {args.output_path}")
    print(f"Summary written to: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
