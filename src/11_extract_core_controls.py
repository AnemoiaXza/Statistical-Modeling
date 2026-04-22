import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import RAW_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text
from stat_modeling.data.pku import load_pku_prefecture_panel
from stat_modeling.data.yearbook_core_controls import build_core_controls_panel


YEARBOOK_ROOT = RAW_DATA_DIR / "2026-04-13_统计建模数据" / "中国统计年鉴原始数据" / "中国统计年鉴" / "Excel版本"
DEFAULT_PKU_PATH = (
    RAW_DATA_DIR
    / "2026-04-13_统计建模数据"
    / "北大数字普惠金融指数"
    / "北京大学数字普惠金融指数（PKU-DFIIC）2011-2023.xlsx"
)
MODELING_INTERIM_DIR = INTERIM_DATA_DIR / "modeling"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract first-batch low-dispute core controls from city yearbooks.")
    parser.add_argument("--yearbook-root", type=Path, default=YEARBOOK_ROOT)
    parser.add_argument("--pku-path", type=Path, default=DEFAULT_PKU_PATH)
    parser.add_argument("--summary-name", default="core_controls_extract_summary.txt")
    return parser


def run_extract(args: argparse.Namespace) -> dict[str, Path]:
    ensure_project_directories()
    MODELING_INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    pku_reference = load_pku_prefecture_panel(args.pku_path, year_min=2019, year_max=2023)[
        ["pku_city_code", "pku_city_name_cn", "pku_city_name_eng", "year"]
    ].drop_duplicates(subset=["pku_city_code", "pku_city_name_cn", "pku_city_name_eng"])
    controls = build_core_controls_panel(args.yearbook_root, pku_reference)
    output_path = MODELING_INTERIM_DIR / "core_controls_candidate_2019_2023.csv"
    write_table(controls, output_path)
    summary = "\n".join(
        [
            "Core Controls Extract Summary",
            f"output: {output_path}",
            f"rows: {len(controls)}",
            f"city_count: {controls['pku_city_code'].nunique()}",
            f"years: {sorted(controls['year'].unique().tolist())}",
            f"columns: {controls.columns.tolist()}",
        ]
    ) + "\n"
    summary_path = write_text(summary, INTERIM_DATA_DIR / args.summary_name)
    return {"output_path": output_path, "summary_path": summary_path}


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    outputs = run_extract(args)
    print(f"Controls output: {outputs['output_path']}")
    print(f"Summary written to: {outputs['summary_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
