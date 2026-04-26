from pathlib import Path

RANDOM_SEED = 42


def _resolve_project_root() -> Path:
    current_file = Path(__file__).resolve()
    for parent in current_file.parents:
        if parent.name == ".worktrees":
            return parent.parent
        if parent.name == "worktrees" and len(parent.parents) >= 4 and parent.parents[2].name == ".omx":
            return parent.parents[3]
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


def _policy_text_directories() -> tuple[Path, Path, Path]:
    return (
        INTERIM_DATA_DIR / "policy_text",
        PROCESSED_DATA_DIR / "policy_text",
        LOGS_DIR / "policy_text",
    )


POLICY_TEXT_INTERIM_DIR, POLICY_TEXT_PROCESSED_DIR, POLICY_TEXT_LOGS_DIR = _policy_text_directories()


def get_required_directories() -> tuple[Path, ...]:
    policy_text_interim, policy_text_processed, policy_text_logs = _policy_text_directories()
    return (
        RAW_DATA_DIR,
        INTERIM_DATA_DIR,
        PROCESSED_DATA_DIR,
        TABLES_DIR,
        FIGURES_DIR,
        LOGS_DIR,
        DOCS_PLANS_DIR,
        policy_text_interim,
        policy_text_processed,
        policy_text_logs,
    )


REQUIRED_DIRECTORIES = get_required_directories()


def ensure_project_directories() -> list[Path]:
    created_or_existing: list[Path] = []
    for directory in get_required_directories():
        directory.mkdir(parents=True, exist_ok=True)
        created_or_existing.append(directory)
    return created_or_existing
