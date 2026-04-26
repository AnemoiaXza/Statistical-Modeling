import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text
from stat_modeling.policy_text.mechanism_panel import build_policy_mechanism_template


DEFAULT_INPUT_PATH = INTERIM_DATA_DIR / "modeling" / "modeling_candidate_panel_2019_2023.csv"
DEFAULT_OUTPUT_PATH = INTERIM_DATA_DIR / "policy_text" / "policy_mechanism_template_2019_2023.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a city-year policy mechanism template aligned to the modeling panel.")
    parser.add_argument("--input-path", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-path", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--summary-name", default="policy_mechanism_template_summary.txt")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_project_directories()
    base = read_table(args.input_path)
    template = build_policy_mechanism_template(base)
    write_table(template, args.output_path)
    summary = "\n".join(
        [
            "Policy Mechanism Template Summary",
            f"input_path: {args.input_path}",
            f"output_path: {args.output_path}",
            f"rows: {len(template)}",
            f"city_count: {template['pku_city_code'].nunique()}",
            "columns: year,pku_city_code,pku_city_name_cn,policy_strength,execution_clarity,digital_green_synergy,policy_doc_count,mechanism_data_status",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / args.summary_name)
    print(f"Policy mechanism template written to: {args.output_path}")
    print(f"Summary written to: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
