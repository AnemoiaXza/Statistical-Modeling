import argparse
import importlib.util
from pathlib import Path
from typing import Sequence

from stat_modeling.config import INTERIM_DATA_DIR
from stat_modeling.config import LOGS_DIR
from stat_modeling.config import RANDOM_SEED
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import read_table
from stat_modeling.data.io import write_table
from stat_modeling.data.io import write_text
from stat_modeling.modeling.heterogeneity import build_heterogeneity_input
from stat_modeling.modeling.heterogeneity import compute_feature_correlation
from stat_modeling.modeling.heterogeneity import fit_candidate_cate
from stat_modeling.modeling.heterogeneity import parse_feature_columns
from stat_modeling.modeling.heterogeneity import validate_feature_columns


DEFAULT_INPUT_PATH = INTERIM_DATA_DIR / "modeling" / "dml_candidate_input_2019_2023.csv"
DEFAULT_OUTPUT_PATH = INTERIM_DATA_DIR / "modeling" / "heterogeneity_candidate_input.csv"
DEFAULT_CORR_PATH = INTERIM_DATA_DIR / "modeling" / "heterogeneity_feature_correlation.csv"
DEFAULT_CATE_PATH = INTERIM_DATA_DIR / "modeling" / "heterogeneity_candidate_cate.csv"
DEFAULT_CATE_SUMMARY_PATH = INTERIM_DATA_DIR / "modeling" / "heterogeneity_candidate_cate_summary.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare heterogeneity candidate inputs and feature diagnostics.")
    parser.add_argument("--input-path", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-path", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--correlation-path", type=Path, default=DEFAULT_CORR_PATH)
    parser.add_argument("--cate-output-path", type=Path, default=DEFAULT_CATE_PATH)
    parser.add_argument("--cate-summary-path", type=Path, default=DEFAULT_CATE_SUMMARY_PATH)
    parser.add_argument("--summary-name", default="heterogeneity_input_summary.txt")
    parser.add_argument("--list-columns", action="store_true")
    parser.add_argument("--check-deps", action="store_true", help="Only check heterogeneity runtime dependencies and exit.")
    parser.add_argument("--treatment-column", default="digital_inclusive_finance_index")
    parser.add_argument("--outcome-column", default="co2_emission_intensity")
    parser.add_argument("--control-columns", default="", help="Comma-separated control columns for candidate CATE fitting.")
    parser.add_argument("--fit-cate", action="store_true", help="Fit a candidate CATE model when econml/shap runtime is available.")
    parser.add_argument(
        "--feature-columns",
        default="gdp_total,secondary_industry_share,fiscal_expenditure",
        help="Comma-separated candidate heterogeneity feature columns.",
    )
    return parser


def dependency_status() -> dict[str, bool]:
    return {
        "econml": bool(importlib.util.find_spec("econml")),
        "shap": bool(importlib.util.find_spec("shap")),
        "sklearn": bool(importlib.util.find_spec("sklearn")),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_project_directories()
    frame = read_table(args.input_path)
    deps = dependency_status()
    if args.list_columns:
        for column in frame.columns:
            print(column)
        return 0
    if args.check_deps:
        for name, available in deps.items():
            print(f"{name}={available}")
        return 0

    feature_columns = parse_feature_columns(args.feature_columns)
    control_columns = parse_feature_columns(args.control_columns)
    validate_feature_columns(frame, feature_columns)
    if args.fit_cate:
        validate_feature_columns(frame, control_columns)
    heterogeneity_input = build_heterogeneity_input(
        frame=frame,
        treatment_column=args.treatment_column,
        outcome_column=args.outcome_column,
        feature_columns=feature_columns,
    )
    correlation = compute_feature_correlation(frame, feature_columns)
    write_table(heterogeneity_input, args.output_path)
    correlation.to_csv(args.correlation_path, index=True)

    summary = "\n".join(
        [
            "Heterogeneity Input Summary",
            f"input_path: {args.input_path}",
            f"output_path: {args.output_path}",
            f"correlation_path: {args.correlation_path}",
            f"rows: {len(heterogeneity_input)}",
            f"city_count: {heterogeneity_input['pku_city_code'].nunique()}",
            f"feature_columns: {feature_columns}",
            f"dependency_status: {deps}",
            "boundary_note: choosing headline heterogeneity features remains a research-design decision; this script only prepares candidate inputs.",
        ]
    ) + "\n"
    summary_path = write_text(summary, LOGS_DIR / args.summary_name)
    print(f"Heterogeneity summary written to: {summary_path}")
    print(f"Heterogeneity input written to: {args.output_path}")
    print(f"Feature correlation written to: {args.correlation_path}")
    if args.fit_cate and (not deps["econml"] or not deps["shap"]):
        blocker_text = "\n".join(
            [
                "Heterogeneity Runtime Blocker",
                f"econml_available: {deps['econml']}",
                f"shap_available: {deps['shap']}",
                "status: ready for candidate-input preparation, blocked for full CATE/SHAP execution until dependencies are installed",
            ]
        ) + "\n"
        blocker_path = write_text(blocker_text, LOGS_DIR / "heterogeneity_runtime_blocker.txt")
        print(f"Heterogeneity blocker written to: {blocker_path}")
        return 1
    if args.fit_cate:
        cate_frame, cate_summary = fit_candidate_cate(
            frame=frame,
            treatment_column=args.treatment_column,
            outcome_column=args.outcome_column,
            feature_columns=feature_columns,
            control_columns=control_columns,
            random_seed=RANDOM_SEED,
        )
        write_table(cate_frame, args.cate_output_path)
        write_table(cate_summary.to_frame(), args.cate_summary_path)
        print(f"CATE output written to: {args.cate_output_path}")
        print(f"CATE summary written to: {args.cate_summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
