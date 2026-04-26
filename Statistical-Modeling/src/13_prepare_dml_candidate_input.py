import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.dml_input import build_dml_candidate_input
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text


DEFAULT_PANEL_PATH = INTERIM_DATA_DIR / "modeling" / "modeling_candidate_panel_2019_2023.csv"
DEFAULT_OUTPUT_PATH = INTERIM_DATA_DIR / "modeling" / "dml_candidate_input_2019_2023.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare DML candidate input panel from the modeling candidate panel.")
    parser.add_argument("--panel-path", type=Path, default=DEFAULT_PANEL_PATH)
    parser.add_argument("--output-path", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--summary-name", default="dml_candidate_input_summary.txt")
    return parser


def run_prepare(args: argparse.Namespace) -> dict[str, Path]:
    ensure_project_directories()
    panel = read_table(args.panel_path)
    dml_panel = build_dml_candidate_input(panel)
    write_table(dml_panel, args.output_path)
    summary = "\n".join(
        [
            "DML Candidate Input Summary",
            f"output: {args.output_path}",
            f"rows: {len(dml_panel)}",
            f"city_count: {dml_panel['pku_city_code'].nunique()}",
            "boundary_note: `population_control_candidate` is still a candidate control variable sourced from cross-year mixed population definitions; do not treat it as a final locked control in the paper without explicit confirmation.",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / args.summary_name)
    return {"output_path": args.output_path, "summary_path": summary_path}


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    outputs = run_prepare(args)
    print(f"DML candidate input: {outputs['output_path']}")
    print(f"Summary written to: {outputs['summary_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
