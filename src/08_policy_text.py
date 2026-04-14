from __future__ import annotations

import argparse

from stat_modeling.config import ensure_project_directories


STAGES = ("discover", "normalize", "rules", "aggregate")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Policy text corpus pipeline for mechanism and moderation analysis.",
    )
    parser.add_argument("--stage", choices=STAGES, help="Optional pipeline stage to run.")
    parser.add_argument("--year", type=int, help="Optional discovery year for targeted runs.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    ensure_project_directories()

    if args.stage:
        print(f"Prepared policy text stage: {args.stage}")
    else:
        print("Policy text corpus pipeline scaffold is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
