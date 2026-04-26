# Research Project Bootstrap Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a reproducible, Git-managed Python research scaffold for the statistical modeling competition, including the first-stage data cleaning pipeline skeleton.

**Architecture:** Use a `B-lite` structure. Numbered scripts under `src/` remain workflow entrypoints for the paper, while reusable logic lives in `src/stat_modeling/`. The cleaning pipeline must be testable, fail fast on invalid inputs, and write outputs through staged directories from raw to interim to processed.

**Tech Stack:** Python 3.11, conda, pandas, numpy, scipy, scikit-learn, econml, doubleml, shap, statsmodels, linearmodels, matplotlib, seaborn, pytest.

---

### Task 1: Package Scaffold and Repository Metadata

**Files:**
- Create: `.gitignore`
- Create: `README.md`
- Create: `environment.yml`
- Create: `src/stat_modeling/__init__.py`
- Create: `src/stat_modeling/config.py`
- Create: `tests/test_config.py`

**Step 1: Write the failing test**

```python
from stat_modeling.config import PROJECT_ROOT, RANDOM_SEED


def test_project_root_points_to_repository_root():
    assert PROJECT_ROOT.name == "Statistical-Modeling"
    assert RANDOM_SEED == 42
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py -v`
Expected: FAIL with `ModuleNotFoundError` or missing attributes.

**Step 3: Write minimal implementation**

- Create `src/stat_modeling/__init__.py`
- Implement `src/stat_modeling/config.py` with:
  - `RANDOM_SEED = 42`
  - root-relative path constants
  - helper to create required directories
- Add `.gitignore` for Python caches, local environments, logs, and generated outputs that should not be versioned
- Add `README.md` with project overview, setup, and run order
- Add `environment.yml` with pinned package versions

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RANDOM_SEED = 42
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_config.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add .gitignore README.md environment.yml src/stat_modeling/__init__.py src/stat_modeling/config.py tests/test_config.py
git commit -m "feat: bootstrap project metadata and config"
```

### Task 2: Data I/O and Path Safety Helpers

**Files:**
- Create: `src/stat_modeling/data/__init__.py`
- Create: `src/stat_modeling/data/io.py`
- Create: `tests/test_data_io.py`

**Step 1: Write the failing test**

```python
import pandas as pd

from stat_modeling.data.io import write_table


def test_write_table_creates_parent_directory(tmp_path):
    frame = pd.DataFrame({"city_code": [110100], "year": [2011]})
    output = tmp_path / "nested" / "panel.csv"
    write_table(frame, output)
    assert output.exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_io.py -v`
Expected: FAIL with import error or missing function.

**Step 3: Write minimal implementation**

- Implement read/write helpers in `src/stat_modeling/data/io.py`
- Support `.csv`, `.parquet`, and summary text output
- Validate supported file suffixes and create parent directories automatically

```python
def write_table(frame, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_io.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/data/__init__.py src/stat_modeling/data/io.py tests/test_data_io.py
git commit -m "feat: add data io helpers"
```

### Task 3: Cleaning Primitives

**Files:**
- Create: `src/stat_modeling/data/cleaning.py`
- Create: `tests/test_data_cleaning.py`

**Step 1: Write the failing tests**

```python
import pandas as pd

from stat_modeling.data.cleaning import interpolate_by_group, winsorize_series


def test_winsorize_series_caps_extreme_values():
    values = pd.Series([1, 2, 3, 100])
    result = winsorize_series(values, lower=0.0, upper=0.75)
    assert result.max() == 3


def test_interpolate_by_group_fills_internal_missing_values():
    frame = pd.DataFrame(
        {"city_code": [1, 1, 1], "year": [2011, 2012, 2013], "value": [1.0, None, 3.0]}
    )
    result = interpolate_by_group(frame, group_key="city_code", order_key="year", columns=["value"])
    assert result.loc[result["year"] == 2012, "value"].iat[0] == 2.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_cleaning.py -v`
Expected: FAIL with import error or missing functions.

**Step 3: Write minimal implementation**

- Implement percentile-based winsorization for continuous variables
- Implement grouped linear interpolation sorted by year
- Keep functions pure and reusable

```python
def winsorize_series(series, lower=0.01, upper=0.99):
    lower_bound = series.quantile(lower)
    upper_bound = series.quantile(upper)
    return series.clip(lower=lower_bound, upper=upper_bound)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_cleaning.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/data/cleaning.py tests/test_data_cleaning.py
git commit -m "feat: add cleaning primitives"
```

### Task 4: Merge Logic and Validation Rules

**Files:**
- Create: `src/stat_modeling/data/merge.py`
- Modify: `src/stat_modeling/data/cleaning.py`
- Create: `tests/test_merge.py`

**Step 1: Write the failing test**

```python
import pandas as pd
import pytest

from stat_modeling.data.merge import assert_unique_panel_keys


def test_assert_unique_panel_keys_raises_for_duplicates():
    frame = pd.DataFrame({"city_code": [1, 1], "year": [2011, 2011]})
    with pytest.raises(ValueError):
        assert_unique_panel_keys(frame, keys=["city_code", "year"])
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_merge.py -v`
Expected: FAIL with import error or missing function.

**Step 3: Write minimal implementation**

- Add unique-key validation
- Add outer/left merge helpers for multiple source tables
- Add balanced-panel helper that expands city-year combinations
- Add cleaning summary generator with row counts and missingness diagnostics

```python
def assert_unique_panel_keys(frame, keys):
    if frame.duplicated(keys).any():
        raise ValueError("Duplicate panel keys detected")
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_merge.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/data/merge.py src/stat_modeling/data/cleaning.py tests/test_merge.py
git commit -m "feat: add merge validation helpers"
```

### Task 5: Cleaning Pipeline Entrypoint

**Files:**
- Create: `src/01_data_clean.py`
- Create: `tests/test_data_clean_pipeline_smoke.py`
- Create: `data/codebook.md`

**Step 1: Write the failing smoke test**

```python
from pathlib import Path
from subprocess import run


def test_data_clean_script_runs_with_sample_inputs(tmp_path):
    result = run(["python", "src/01_data_clean.py", "--help"], cwd=Path.cwd(), capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_clean_pipeline_smoke.py -v`
Expected: FAIL because the script does not exist yet.

**Step 3: Write minimal implementation**

- Implement CLI argument parsing in `src/01_data_clean.py`
- Wire the entrypoint to package functions
- Emit placeholder cleaning summary and target output paths
- Create `data/codebook.md` template with variable metadata columns

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_clean_pipeline_smoke.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/01_data_clean.py tests/test_data_clean_pipeline_smoke.py data/codebook.md
git commit -m "feat: add cleaning pipeline entrypoint"
```

### Task 6: Full Verification and Documentation Review

**Files:**
- Modify: `README.md`
- Modify: `environment.yml`
- Modify: `data/codebook.md`
- Modify: `src/01_data_clean.py`
- Modify: `src/stat_modeling/config.py`
- Modify: `src/stat_modeling/data/io.py`
- Modify: `src/stat_modeling/data/cleaning.py`
- Modify: `src/stat_modeling/data/merge.py`
- Modify: `tests/test_config.py`
- Modify: `tests/test_data_io.py`
- Modify: `tests/test_data_cleaning.py`
- Modify: `tests/test_merge.py`
- Modify: `tests/test_data_clean_pipeline_smoke.py`

**Step 1: Run the full test suite**

Run: `pytest tests -v`
Expected: PASS with all tests green.

**Step 2: Run a lightweight repository sanity check**

Run: `python -m compileall src`
Expected: PASS with no syntax errors.

**Step 3: Review README and codebook for consistency**

- Confirm run order matches the numbered script workflow
- Confirm `RANDOM_SEED = 42` appears in docs and code
- Confirm codebook template matches agreed metadata fields

**Step 4: Commit**

```bash
git add README.md environment.yml data/codebook.md src tests
git commit -m "test: verify bootstrap scaffold"
```
