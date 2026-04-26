import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text
from stat_modeling.policy_text.bootstrap import build_policy_city_year_scores_template
from stat_modeling.policy_text.bootstrap import build_policy_document_registry_template
from stat_modeling.policy_text.bootstrap import build_policy_source_manifest


DEFAULT_BASE_PANEL = INTERIM_DATA_DIR / "modeling" / "modeling_candidate_panel_2019_2023.csv"
POLICY_TEXT_DIR = INTERIM_DATA_DIR / "policy_text"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare policy-text bootstrap artifacts.")
    parser.add_argument("--base-panel-path", type=Path, default=DEFAULT_BASE_PANEL)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_project_directories()
    POLICY_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    base_panel = read_table(args.base_panel_path)
    source_manifest = build_policy_source_manifest()
    registry_template = build_policy_document_registry_template()
    city_year_template = build_policy_city_year_scores_template(base_panel)

    source_path = POLICY_TEXT_DIR / "policy_source_manifest.csv"
    registry_path = POLICY_TEXT_DIR / "policy_document_registry_template.csv"
    city_year_path = POLICY_TEXT_DIR / "policy_city_year_scores_template.csv"

    write_table(source_manifest, source_path)
    write_table(registry_template, registry_path)
    write_table(city_year_template, city_year_path)

    summary = "\n".join(
        [
            "Policy Text Bootstrap Summary",
            f"source_manifest: {source_path}",
            f"registry_template: {registry_path}",
            f"city_year_scores_template: {city_year_path}",
            f"city_year_rows: {len(city_year_template)}",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / "policy_text_bootstrap_summary.txt")
    print(f"Policy source manifest written to: {source_path}")
    print(f"Policy document registry template written to: {registry_path}")
    print(f"Policy city-year scores template written to: {city_year_path}")
    print(f"Summary written to: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
