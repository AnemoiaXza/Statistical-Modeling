import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import LOGS_DIR
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text


DEFAULT_INPUT_PATH = INTERIM_DATA_DIR / "modeling" / "dml_candidate_input_2019_2023.csv"
DEFAULT_OUTPUT_PATH = INTERIM_DATA_DIR / "modeling" / "dml_run_input.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare and summarize DML candidate inputs before model fitting."
    )
    parser.add_argument("--input-path", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-path", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--summary-name", default="dml_input_readiness_summary.txt")
    parser.add_argument("--list-columns", action="store_true", help="Print available input columns and exit.")
    parser.add_argument("--treatment-column", default="digital_inclusive_finance_index")
    parser.add_argument("--outcome-column", default="co2_emission_intensity")
    parser.add_argument(
        "--control-columns",
        default="",
        help="Comma-separated control columns to require for the run input table.",
    )
    return parser


def parse_control_columns(raw_value: str) -> list[str]:
    return [value.strip() for value in raw_value.split(",") if value.strip()]


def validate_required_columns(frame_columns: list[str], required_columns: list[str]) -> None:
    missing = [column for column in required_columns if column not in frame_columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def build_summary(
    input_path: Path,
    frame,
    treatment_column: str,
    outcome_column: str,
    control_columns: list[str],
    filtered_row_count: int | None = None,
) -> str:
    lines = [
        "DML Input Readiness Summary",
        f"input_path: {input_path}",
        f"rows: {len(frame)}",
        f"city_count: {frame['pku_city_code'].nunique()}",
        f"years: {sorted(frame['year'].unique().tolist())}",
        f"treatment_column: {treatment_column}",
        f"main_outcome_column: {outcome_column}",
        f"robustness_outcome_column: co2_emission_total",
        f"control_columns: {control_columns}",
        "required_non_missing_columns:",
    ]
    required = [
        treatment_column,
        outcome_column,
        "co2_emission_total",
    ] + control_columns
    required = list(dict.fromkeys(required))
    for column in required:
        lines.append(f"- {column}: missing={int(frame[column].isna().sum())}")
    if filtered_row_count is not None:
        lines.append(f"filtered_row_count: {filtered_row_count}")
    lines.append(
        "boundary_note: population_control_candidate is still a candidate control variable with unresolved cross-year source-definition differences."
    )
    return "\n".join(lines) + "\n"


def prepare_run_input(frame, treatment_column: str, outcome_column: str, control_columns: list[str]):
    required = [treatment_column, outcome_column] + control_columns
    required = list(dict.fromkeys(required))
    return frame.dropna(subset=required).reset_index(drop=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_project_directories()
    frame = read_table(args.input_path)
    if args.list_columns:
        for column in frame.columns:
            print(column)
        return 0

    control_columns = parse_control_columns(args.control_columns)
    validate_required_columns(
        list(frame.columns),
        [args.treatment_column, args.outcome_column, "co2_emission_total"] + control_columns,
    )
    filtered = prepare_run_input(frame, args.treatment_column, args.outcome_column, control_columns)
    if control_columns:
        write_table(filtered, args.output_path)
    summary = build_summary(
        args.input_path,
        frame,
        treatment_column=args.treatment_column,
        outcome_column=args.outcome_column,
        control_columns=control_columns,
        filtered_row_count=len(filtered),
    )
    summary_path = write_text(summary, LOGS_DIR / args.summary_name)
    print(f"DML input summary written to: {summary_path}")
    if control_columns:
        print(f"Filtered DML run input written to: {args.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
