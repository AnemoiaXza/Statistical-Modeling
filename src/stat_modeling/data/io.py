from pathlib import Path

import pandas as pd

SUPPORTED_TABLE_SUFFIXES = {".csv", ".parquet"}


def _normalize_path(path: str | Path) -> Path:
    return Path(path)


def read_table(path: str | Path) -> pd.DataFrame:
    input_path = _normalize_path(path)
    if input_path.suffix not in SUPPORTED_TABLE_SUFFIXES:
        raise ValueError(f"Unsupported table format: {input_path.suffix}")

    if input_path.suffix == ".csv":
        return pd.read_csv(input_path)

    return pd.read_parquet(input_path)


def write_table(frame: pd.DataFrame, output_path: str | Path) -> Path:
    destination = _normalize_path(output_path)
    if destination.suffix not in SUPPORTED_TABLE_SUFFIXES:
        raise ValueError(f"Unsupported table format: {destination.suffix}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.suffix == ".csv":
        frame.to_csv(destination, index=False)
    else:
        frame.to_parquet(destination, index=False)
    return destination


def write_text(text: str, output_path: str | Path) -> Path:
    destination = _normalize_path(output_path)
    if destination.suffix != ".txt":
        raise ValueError(f"Unsupported text format: {destination.suffix}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    return destination
