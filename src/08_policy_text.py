import argparse
from pathlib import Path
from typing import Sequence

from stat_modeling.config import PROJECT_ROOT
from stat_modeling.config import ensure_project_directories
from stat_modeling.data.io import write_text


POLICY_TEXT_INTERIM_DIR = PROJECT_ROOT / "data" / "interim" / "policy_text"
POLICY_TEXT_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "policy_text"
POLICY_TEXT_LOGS_DIR = PROJECT_ROOT / "logs" / "policy_text"
SUPPORTED_STAGES = ("discover", "normalize", "rules", "score", "aggregate", "full")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Policy-text corpus pipeline scaffold for mechanism/moderation analysis. "
            "The workflow discovers, normalizes, scores, and aggregates policy documents "
            "into city-year outputs without changing the main causal identification route."
        )
    )
    parser.add_argument(
        "--stage",
        choices=SUPPORTED_STAGES,
        default="full",
        help="Pipeline stage to prepare or execute.",
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=2020,
        help="Inclusive lower bound for policy discovery.",
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=2024,
        help="Inclusive upper bound for policy discovery.",
    )
    parser.add_argument(
        "--summary-name",
        default="implementation_summary.txt",
        help="Summary filename written under logs/policy_text/.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write a handoff summary only; do not invoke downstream implementation hooks.",
    )
    return parser


def build_summary(args: argparse.Namespace) -> str:
    lines = [
        "Policy Text Pipeline Summary",
        f"stage: {args.stage}",
        f"year_window: {args.start_year}-{args.end_year}",
        f"dry_run: {args.dry_run}",
        "research_role: mechanism/moderation only",
        f"interim_dir: {POLICY_TEXT_INTERIM_DIR}",
        f"processed_dir: {POLICY_TEXT_PROCESSED_DIR}",
        f"logs_dir: {POLICY_TEXT_LOGS_DIR}",
        "supported_outputs:",
        "- corpus metadata table",
        "- normalized policy text artifacts",
        "- rule/LLM feature tables",
        "- city-year aggregate panels",
    ]
    return "\n".join(lines) + "\n"


def run_policy_text_pipeline(args: argparse.Namespace) -> dict[str, Path | str | bool]:
    ensure_project_directories()
    POLICY_TEXT_INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    POLICY_TEXT_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    POLICY_TEXT_LOGS_DIR.mkdir(parents=True, exist_ok=True)

    summary_text = build_summary(args)
    summary_path = write_text(summary_text, POLICY_TEXT_LOGS_DIR / args.summary_name)

    return {
        "stage": args.stage,
        "dry_run": args.dry_run,
        "summary_path": summary_path,
        "interim_dir": POLICY_TEXT_INTERIM_DIR,
        "processed_dir": POLICY_TEXT_PROCESSED_DIR,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    results = run_policy_text_pipeline(args)

    print(f"Summary written to: {results['summary_path']}")
    print(f"Interim workspace: {results['interim_dir']}")
    print(f"Processed workspace: {results['processed_dir']}")
    print(f"Selected stage: {results['stage']}")
    if results["dry_run"]:
        print("Dry run only. No downstream policy-text execution hooks were invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
