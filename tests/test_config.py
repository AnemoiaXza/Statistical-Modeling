from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stat_modeling.config import PROJECT_ROOT, RANDOM_SEED


def test_project_root_points_to_repository_root():
    assert PROJECT_ROOT.name == "Statistical-Modeling"
    assert RANDOM_SEED == 42
