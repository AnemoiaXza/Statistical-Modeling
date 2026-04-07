import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import LOGS_DIR
from stat_modeling.config import PROCESSED_DATA_DIR
from stat_modeling.config import RAW_DATA_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import write_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare the staged data-cleaning workspace for panel-data construction."
    )
    parser.add_argument(
        "--input-pattern",
        default="*",
        help="Glob pattern used to discover raw source files under data/raw/.",
    )
    parser.add_argument(
        "--summary-name",
        default="data_clean_summary.txt",
        help="Summary filename written under logs/.",
    )
    parser.add_argument(
        "--output-stem",
        default="panel_data",
        help="Target stem for processed outputs under data/processed/.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Discover inputs and write summary only, without creating placeholder tables.",
    )
    return parser


def discover_source_files(pattern: str) -> list[Path]:
    return sorted(path for path in RAW_DATA_DIR.glob(pattern) if path.is_file())


def build_cleaning_summary(
    source_files: Sequence[Path],
    output_stem: str,
    dry_run: bool,
) -> str:
    interim_target = INTERIM_DATA_DIR / "panel_interim_raw_scan.parquet"
    processed_csv_target = PROCESSED_DATA_DIR / f"{output_stem}.csv"
    processed_parquet_target = PROCESSED_DATA_DIR / f"{output_stem}.parquet"

    lines = [
        "Data Cleaning Pipeline Summary",
        f"raw_source_count: {len(source_files)}",
        f"dry_run: {dry_run}",
        f"interim_target: {interim_target}",
        f"processed_csv_target: {processed_csv_target}",
        f"processed_parquet_target: {processed_parquet_target}",
    ]
    if source_files:
        lines.append("discovered_sources:")
        lines.extend(f"- {path}" for path in source_files)
    else:
        lines.append("discovered_sources: none")
        lines.append("note: source-file mappings will be filled once raw data is delivered.")
    return "\n".join(lines) + "\n"


def run_cleaning_pipeline(args: argparse.Namespace) -> dict[str, Path | list[Path]]:
    ensure_project_directories()
    source_files = discover_source_files(args.input_pattern)
    summary_text = build_cleaning_summary(source_files, args.output_stem, args.dry_run)
    summary_path = write_text(summary_text, LOGS_DIR / args.summary_name)

    return {
        "summary_path": summary_path,
        "source_files": source_files,
        "interim_output_path": INTERIM_DATA_DIR / "panel_interim_raw_scan.parquet",
        "processed_csv_output_path": PROCESSED_DATA_DIR / f"{args.output_stem}.csv",
        "processed_parquet_output_path": PROCESSED_DATA_DIR / f"{args.output_stem}.parquet",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    results = run_cleaning_pipeline(args)

    print(f"Summary written to: {results['summary_path']}")
    print(f"Interim output target: {results['interim_output_path']}")
    print(f"Processed CSV target: {results['processed_csv_output_path']}")
    print(f"Processed Parquet target: {results['processed_parquet_output_path']}")
    if not results["source_files"]:
        print("No raw files discovered. Pipeline scaffold only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
