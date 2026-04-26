import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text
from stat_modeling.data.mechanism_merge import merge_modeling_with_policy_seed


DEFAULT_MODELING = INTERIM_DATA_DIR / "modeling" / "modeling_candidate_panel_2019_2023.csv"
DEFAULT_POLICY = INTERIM_DATA_DIR / "policy_text" / "policy_mechanism_seed_panel_2019_2023.csv"
DEFAULT_OUTPUT = INTERIM_DATA_DIR / "modeling" / "modeling_candidate_panel_with_policy_seed_2019_2023.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge modeling candidate panel with seeded policy mechanism panel.")
    parser.add_argument("--modeling-path", type=Path, default=DEFAULT_MODELING)
    parser.add_argument("--policy-path", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--output-path", type=Path, default=DEFAULT_OUTPUT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_project_directories()
    modeling = read_table(args.modeling_path)
    policy = read_table(args.policy_path)
    merged = merge_modeling_with_policy_seed(modeling, policy)
    write_table(merged, args.output_path)
    summary = "\n".join(
        [
            "Modeling + Policy Seed Panel Summary",
            f"output_path: {args.output_path}",
            f"rows: {len(merged)}",
            f"city_count: {merged['pku_city_code'].nunique()}",
            f"nonzero_policy_doc_rows: {int((merged['policy_doc_count'].fillna(0) > 0).sum())}",
            "boundary_note: policy columns are currently seeded central rule-proxy values, not final policy-text scores.",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / "modeling_policy_seed_panel_summary.txt")
    print(f"Merged panel written to: {args.output_path}")
    print(f"Summary written to: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
