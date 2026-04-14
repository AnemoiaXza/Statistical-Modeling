# Statistical Modeling Competition Project

## Overview

This repository contains the implementation workflow for the 2026 statistical modeling competition topic:

"Dual-carbon strategy and the carbon reduction effect of digital economy: causal inference and heterogeneity analysis based on double machine learning."

The project uses a `B-lite` structure:

- Numbered scripts under `src/` map to research steps.
- Reusable logic lives in `src/stat_modeling/`.
- Policy-text features remain an auxiliary mechanism/moderation lane; they do not replace the main identification design.

## Setup

Create the conda environment:

```bash
conda env create -f environment.yml
conda activate stat-modeling
```

## Reproducibility

- Global random seed: `RANDOM_SEED = 42`
- Required directories are managed by `stat_modeling.config.ensure_project_directories()`
- Policy-text artifacts are stored under `data/interim/policy_text`, `data/processed/policy_text`, and `logs/policy_text`
- Raw HTML pages and downloaded attachments are organized beneath `data/interim/policy_text/raw_html` and `data/interim/policy_text/attachments`

## Policy Text Module

Use the policy-text scaffold when you need reproducible document discovery, normalization, rule extraction, scoring payload preparation, and `city-year` aggregation for the approved double-carbon corpus window.

```bash
python3 src/08_policy_text.py --help
```

## Planned Run Order

1. `src/01_data_clean.py`
2. `src/02_dea_efficiency.py`
3. `src/03_eda.py`
4. `src/04_dml_main.py`
5. `src/05_heterogeneity.py`
6. `src/06_robustness.py`
7. `src/07_spatial.py` (optional)
8. `src/08_policy_text.py` (mechanism/moderation support lane)

## Policy-text corpus lane

Use the policy-text scaffold to prepare the corpus workspace and record the expected pipeline stage:

```bash
python3 src/08_policy_text.py --help
python3 src/08_policy_text.py --stage discover --dry-run
```

Current scaffold behavior:

- creates the policy-text interim / processed / log folders when missing
- writes a UTF-8 summary under `logs/policy_text/`
- keeps the policy-text module scoped to mechanism and moderation analysis rather than the headline treatment effect

Planned policy-text stages:

- `discover` — identify candidate policy documents on approved official sites
- `normalize` — standardize metadata and text capture
- `rules` — extract rule-based indicators such as deadlines or quantitative targets
- `score` — attach validated LLM scoring outputs
- `aggregate` — roll document scores into city-year features
- `full` — run the full staged pipeline once the package implementation is in place
