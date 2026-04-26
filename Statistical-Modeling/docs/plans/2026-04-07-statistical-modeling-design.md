# Statistical Modeling Project Design

## Context

- Competition: 2026 全国大学生统计建模大赛
- Theme: “服务国家战略 创新统计赋能”
- Proposed paper topic: “双碳”战略下数字经济的碳减排效应——基于双重机器学习的因果推断与异质性分析
- Current scope: build a reproducible, Git-managed Python research scaffold before raw data arrives

## Chosen Approach

Adopt a `B-lite` repository design.

- Keep numbered scripts such as `src/01_data_clean.py` to match the paper workflow
- Move reusable logic into a Python package under `src/stat_modeling/`
- Treat scripts as thin entrypoints and keep core logic testable inside package modules

This preserves the research narrative while making collaboration, testing, and later refactoring manageable.

## Repository Architecture

```text
Statistical-Modeling/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── codebook.md
├── docs/
│   └── plans/
├── logs/
├── outputs/
│   ├── figures/
│   └── tables/
├── src/
│   ├── 01_data_clean.py
│   ├── 02_dea_efficiency.py
│   ├── 03_eda.py
│   ├── 04_dml_main.py
│   ├── 05_heterogeneity.py
│   ├── 06_robustness.py
│   ├── 07_spatial.py
│   └── stat_modeling/
│       ├── __init__.py
│       ├── config.py
│       └── data/
│           ├── __init__.py
│           ├── cleaning.py
│           ├── io.py
│           └── merge.py
├── tests/
├── .gitignore
├── README.md
└── environment.yml
```

## Data Flow

The pipeline should remain strictly staged:

`data/raw -> data/interim -> data/processed -> outputs`

Rules:

- `data/raw` is read-only for scripts
- `data/interim` stores temporary harmonized tables and diagnostics
- `data/processed` stores final modeling tables
- `outputs` stores paper-ready figures and tables only
- `logs` stores execution traces and cleaning summaries

## Naming Conventions

- Raw data: `source_topic_yearrange.ext`
- Interim panel tables: `panel_interim_<stage>.parquet`
- Final modeling tables: `panel_data.parquet` and `panel_data.csv`
- Tables: `table_01_descriptive_stats.csv` and `table_01_descriptive_stats.tex`
- Figures: `figure_01_efficiency_trend.pdf`

These conventions make file roles obvious during GitHub collaboration and reduce accidental misuse of intermediate outputs.

## First-Batch Files

The first implementation batch should create:

- `.gitignore`
- `README.md`
- `environment.yml`
- `data/codebook.md`
- `src/01_data_clean.py`
- `src/stat_modeling/__init__.py`
- `src/stat_modeling/config.py`
- `src/stat_modeling/data/io.py`
- `src/stat_modeling/data/cleaning.py`
- `src/stat_modeling/data/merge.py`
- `tests/test_data_cleaning.py`
- one smoke test for the cleaning entrypoint

## Scope of `01_data_clean.py`

`src/01_data_clean.py` should only do the following:

1. Parse configuration and command-line arguments
2. Discover required source files under `data/raw/`
3. Call package-level functions for standardization, merge, and cleaning
4. Write outputs to `data/interim/` and `data/processed/`
5. Export a cleaning summary with sample-size changes and diagnostics

It should not:

- decide unresolved research-design questions
- embed DEA, DML, or heterogeneity logic
- silently skip required inputs
- hardcode special-case handling for unknown future datasets

## Error Handling Policy

- Missing required files: fail fast
- Duplicate `city_code + year` keys: fail fast and export duplicates for inspection
- Invalid data types, out-of-range years, or missing required columns: fail fast
- High missingness: report and mark, but do not auto-decide research deletions beyond agreed rules
- Every run should produce a log and a cleaning summary

## Testing Policy

The first batch should include:

- unit tests for key uniqueness checks
- unit tests for winsorization
- unit tests for linear interpolation
- unit tests for panel balancing helpers
- one end-to-end smoke test for the cleaning entrypoint using toy data

DEA, DML, heterogeneity, and spatial modules are out of scope until input data and variable definitions are available.

## Non-Goals for the First Batch

- No DEA implementation yet
- No DML estimation yet
- No heterogeneity or SHAP analysis yet
- No robustness or spatial workflow yet
- No research-design decisions without user confirmation
