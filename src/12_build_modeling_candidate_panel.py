import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text
from stat_modeling.data.modeling_panel import build_modeling_candidate_panel


DEFAULT_PKU_CMCC_PATH = INTERIM_DATA_DIR / "modeling" / "pku_cmcc_candidate_panel_2019_2023.csv"
DEFAULT_CORE_CONTROLS_PATH = INTERIM_DATA_DIR / "modeling" / "core_controls_candidate_2019_2023.csv"
MODELING_INTERIM_DIR = INTERIM_DATA_DIR / "modeling"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build modeling-ready candidate panel from PKU, CMCC, and core controls.")
    parser.add_argument("--pku-cmcc-path", type=Path, default=DEFAULT_PKU_CMCC_PATH)
    parser.add_argument("--core-controls-path", type=Path, default=DEFAULT_CORE_CONTROLS_PATH)
    parser.add_argument("--summary-name", default="modeling_candidate_panel_summary.txt")
    return parser


def run_build(args: argparse.Namespace) -> dict[str, Path]:
    ensure_project_directories()
    MODELING_INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    pku_cmcc = read_table(args.pku_cmcc_path)
    controls = read_table(args.core_controls_path)
    panel = build_modeling_candidate_panel(pku_cmcc, controls)
    output_path = MODELING_INTERIM_DIR / "modeling_candidate_panel_2019_2023.csv"
    write_table(panel, output_path)
    summary = "\n".join(
        [
            "Modeling Candidate Panel Summary",
            f"output: {output_path}",
            f"rows: {len(panel)}",
            f"city_count: {panel['pku_city_code'].nunique()}",
            f"cmcc_outcome_city_count: {panel.loc[panel['has_cmcc_outcome'], 'pku_city_code'].nunique()}",
            f"core_controls_city_count: {panel.loc[panel['has_core_controls'], 'pku_city_code'].nunique()}",
            f"ready_city_count: {panel.loc[panel['ready_for_dml_candidate'], 'pku_city_code'].nunique()}",
            f"ready_row_count: {int(panel['ready_for_dml_candidate'].sum())}",
            "boundary_note: population_raw is still a candidate control variable with cross-year source-definition risk; do not treat it as final locked control wording in the paper without explicit confirmation.",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / args.summary_name)
    return {"output_path": output_path, "summary_path": summary_path}


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    outputs = run_build(args)
    print(f"Panel output: {outputs['output_path']}")
    print(f"Summary written to: {outputs['summary_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
