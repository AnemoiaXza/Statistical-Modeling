import argparse
from pathlib import Path
from typing import Sequence

import pandas as pd

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import LOGS_DIR
from stat_modeling.config import RAW_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.cmcc import annualize_total_emissions_from_csv
from stat_modeling.data.cmcc import build_resolved_annualized_panel
from stat_modeling.data.cmcc import build_match_candidates
from stat_modeling.data.cmcc import collect_unique_cities
from stat_modeling.data.io import write_text
from stat_modeling.data.pku import load_pku_prefecture_panel


DEFAULT_CMCC_PATH = RAW_DATA_DIR / "2026-04-13_统计建模数据" / "2019-2024 china_city_data_all.csv"
DEFAULT_PKU_PATH = (
    RAW_DATA_DIR
    / "2026-04-13_统计建模数据"
    / "北大数字普惠金融指数"
    / "北京大学数字普惠金融指数（PKU-DFIIC）2011-2023.xlsx"
)
CMCC_INTERIM_DIR = INTERIM_DATA_DIR / "cmcc"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare CMCC annual emissions handoff tables.")
    parser.add_argument("--cmcc-path", type=Path, default=DEFAULT_CMCC_PATH)
    parser.add_argument("--pku-path", type=Path, default=DEFAULT_PKU_PATH)
    parser.add_argument("--max-year", type=int, default=2024)
    parser.add_argument("--summary-name", default="cmcc_prepare_summary.txt")
    return parser

def run_cmcc_prepare(args: argparse.Namespace) -> dict[str, Path]:
    ensure_project_directories()
    CMCC_INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    cmcc_cities = collect_unique_cities(args.cmcc_path)
    pku_reference = (
        load_pku_prefecture_panel(args.pku_path)
        .rename(
            columns={
                "pku_city_name_cn": "pref_name_year18",
                "pku_city_name_eng": "pref_name_year18_eng",
                "pku_city_code": "pref_code_year18",
            }
        )[["pref_name_year18", "pref_name_year18_eng", "pref_code_year18"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    match_candidates = build_match_candidates(cmcc_cities=cmcc_cities, pku_reference=pku_reference)
    annualized = annualize_total_emissions_from_csv(args.cmcc_path, max_year=args.max_year)
    resolved_annualized = build_resolved_annualized_panel(annualized=annualized, match_candidates=match_candidates)

    match_path = CMCC_INTERIM_DIR / "cmcc_pku_city_match_candidates.csv"
    annualized_path = CMCC_INTERIM_DIR / "cmcc_annual_total_emissions.csv"
    matched_annualized_path = CMCC_INTERIM_DIR / "cmcc_annual_total_emissions_matched_candidates.csv"
    resolved_annualized_path = CMCC_INTERIM_DIR / "cmcc_annual_total_emissions_resolved.csv"

    match_candidates.to_csv(match_path, index=False)
    annualized.to_csv(annualized_path, index=False)

    matched_names = set(
        match_candidates.loc[
            match_candidates["match_status"].isin(["direct", "normalized_candidate", "manual_alias"]),
            "cmcc_city",
        ]
    )
    annualized.loc[annualized["city"].isin(matched_names)].to_csv(matched_annualized_path, index=False)
    resolved_annualized.to_csv(resolved_annualized_path, index=False)

    summary_text = "\n".join(
        [
            "CMCC Prepare Summary",
            f"cmcc_path: {args.cmcc_path}",
            f"pku_path: {args.pku_path}",
            f"max_year: {args.max_year}",
            f"match_output: {match_path}",
            f"annualized_output: {annualized_path}",
            f"matched_candidate_output: {matched_annualized_path}",
            f"resolved_output: {resolved_annualized_path}",
            f"match_status_counts: {match_candidates['match_status'].value_counts().to_dict()}",
            f"annualized_rows: {len(annualized)}",
            f"annualized_city_count: {annualized['city'].nunique() if not annualized.empty else 0}",
            f"resolved_rows: {len(resolved_annualized)}",
            f"resolved_city_count: {resolved_annualized['pku_city_code'].nunique() if not resolved_annualized.empty else 0}",
        ]
    ) + "\n"
    summary_path = write_text(summary_text, LOGS_DIR / args.summary_name)

    return {
        "match_path": match_path,
        "annualized_path": annualized_path,
        "matched_annualized_path": matched_annualized_path,
        "resolved_annualized_path": resolved_annualized_path,
        "summary_path": summary_path,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    outputs = run_cmcc_prepare(args)
    print(f"Match candidates: {outputs['match_path']}")
    print(f"Annualized totals: {outputs['annualized_path']}")
    print(f"Matched annualized totals: {outputs['matched_annualized_path']}")
    print(f"Resolved annualized totals: {outputs['resolved_annualized_path']}")
    print(f"Summary written to: {outputs['summary_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
