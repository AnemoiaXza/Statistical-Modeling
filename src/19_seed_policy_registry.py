import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text
from stat_modeling.policy_text.seeds import build_seed_city_year_doc_counts
from stat_modeling.policy_text.seeds import build_seed_registry_frame


DEFAULT_TEMPLATE = INTERIM_DATA_DIR / "policy_text" / "policy_city_year_scores_template.csv"
POLICY_TEXT_DIR = INTERIM_DATA_DIR / "policy_text"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Seed a first central-policy registry and city-year doc-count template.")
    parser.add_argument("--city-year-template", type=Path, default=DEFAULT_TEMPLATE)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_project_directories()
    POLICY_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    registry = build_seed_registry_frame()
    template = read_table(args.city_year_template)
    seeded_scores = build_seed_city_year_doc_counts(registry, template)

    registry_path = POLICY_TEXT_DIR / "policy_document_registry_seed_central.csv"
    seeded_path = POLICY_TEXT_DIR / "policy_city_year_scores_seed_central.csv"
    write_table(registry, registry_path)
    write_table(seeded_scores, seeded_path)

    summary = "\n".join(
        [
            "Policy Seed Registry Summary",
            f"registry_path: {registry_path}",
            f"seeded_city_year_path: {seeded_path}",
            f"registry_docs: {len(registry)}",
            f"seeded_rows: {len(seeded_scores)}",
            f"years_present: {sorted(registry['pub_date'].str[:4].astype(int).unique().tolist())}",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / "policy_seed_registry_summary.txt")
    print(f"Policy seed registry written to: {registry_path}")
    print(f"Seeded city-year scores written to: {seeded_path}")
    print(f"Summary written to: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
