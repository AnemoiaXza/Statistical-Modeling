import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import RAW_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text
from stat_modeling.data.pku import build_pku_cmcc_candidate_panel
from stat_modeling.data.pku import load_pku_prefecture_panel


DEFAULT_PKU_PATH = (
    RAW_DATA_DIR
    / "2026-04-13_统计建模数据"
    / "北大数字普惠金融指数"
    / "北京大学数字普惠金融指数（PKU-DFIIC）2011-2023.xlsx"
)
DEFAULT_CMCC_RESOLVED_PATH = INTERIM_DATA_DIR / "cmcc" / "cmcc_annual_total_emissions_resolved.csv"
PKU_INTERIM_DIR = INTERIM_DATA_DIR / "pku"
MODELING_INTERIM_DIR = INTERIM_DATA_DIR / "modeling"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build PKU panel and CMCC-PKU candidate merged panel.")
    parser.add_argument("--pku-path", type=Path, default=DEFAULT_PKU_PATH)
    parser.add_argument("--cmcc-resolved-path", type=Path, default=DEFAULT_CMCC_RESOLVED_PATH)
    parser.add_argument("--year-min", type=int, default=2019)
    parser.add_argument("--year-max", type=int, default=2023)
    parser.add_argument("--summary-name", default="pku_cmcc_candidate_summary.txt")
    return parser


def run_build(args: argparse.Namespace) -> dict[str, Path]:
    ensure_project_directories()
    PKU_INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    MODELING_INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    pku_panel = load_pku_prefecture_panel(args.pku_path, year_min=args.year_min, year_max=args.year_max)
    cmcc_resolved = read_table(args.cmcc_resolved_path)
    merged = build_pku_cmcc_candidate_panel(
        pku_panel=pku_panel,
        cmcc_resolved_panel=cmcc_resolved,
        year_min=args.year_min,
        year_max=args.year_max,
    )

    pku_output = PKU_INTERIM_DIR / f"pku_prefecture_panel_{args.year_min}_{args.year_max}.csv"
    merged_output = MODELING_INTERIM_DIR / f"pku_cmcc_candidate_panel_{args.year_min}_{args.year_max}.csv"
    write_table(pku_panel, pku_output)
    write_table(merged, merged_output)

    summary = "\n".join(
        [
            "PKU-CMCC Candidate Panel Summary",
            f"pku_output: {pku_output}",
            f"merged_output: {merged_output}",
            f"year_window: {args.year_min}-{args.year_max}",
            f"pku_rows: {len(pku_panel)}",
            f"pku_city_count: {pku_panel['pku_city_code'].nunique()}",
            f"merged_rows: {len(merged)}",
            f"merged_city_count: {merged['pku_city_code'].nunique()}",
            f"cmcc_outcome_city_count: {merged.loc[merged['has_cmcc_outcome'], 'pku_city_code'].nunique()}",
            f"cmcc_outcome_row_count: {int(merged['has_cmcc_outcome'].sum())}",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / args.summary_name)

    return {"pku_output": pku_output, "merged_output": merged_output, "summary_path": summary_path}


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    outputs = run_build(args)
    print(f"PKU output: {outputs['pku_output']}")
    print(f"Merged output: {outputs['merged_output']}")
    print(f"Summary written to: {outputs['summary_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
