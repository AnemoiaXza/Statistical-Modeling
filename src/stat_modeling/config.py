from pathlib import Path

RANDOM_SEED = 42


def _resolve_project_root() -> Path:
    current_file = Path(__file__).resolve()
    for parent in current_file.parents:
        if parent.name == ".worktrees":
            return parent.parent
    return current_file.parents[2]


PROJECT_ROOT = _resolve_project_root()
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
FIGURES_DIR = OUTPUTS_DIR / "figures"
LOGS_DIR = PROJECT_ROOT / "logs"
DOCS_PLANS_DIR = PROJECT_ROOT / "docs" / "plans"

REQUIRED_DIRECTORIES = (
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
    TABLES_DIR,
    FIGURES_DIR,
    LOGS_DIR,
    DOCS_PLANS_DIR,
)


def ensure_project_directories() -> list[Path]:
    created_or_existing: list[Path] = []
    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)
        created_or_existing.append(directory)
    return created_or_existing
