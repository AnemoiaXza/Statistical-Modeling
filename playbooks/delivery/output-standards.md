# Output Standards

## Purpose

This playbook defines how project outputs should be named, stored, and summarized so results remain traceable and ready for paper integration.

## Storage Rules

| Output Type | Location |
| --- | --- |
| Processed modeling tables | `data/processed/` |
| Interim working tables | `data/interim/` |
| Paper-ready tables | `outputs/tables/` |
| Paper-ready figures | `outputs/figures/` |
| Logs and handoff summaries | `logs/` |
| Dataset intake and analysis records | `logs/data_records/` subdirectories |

Raw files remain in `data/raw/` and must not be overwritten.

## Naming Conventions

Use stable, descriptive names.

### Tables

- Descriptive or results tables: `table_XX_short_name.csv`
- LaTeX companion: `table_XX_short_name.tex`
- Example: `table_01_descriptive_stats.csv`

### Figures

- Paper-ready figures: `figure_XX_short_name.pdf`
- Example: `figure_01_efficiency_trend.pdf`

### Processed Data

- Final panel table: `panel_data.parquet`
- Companion export when needed: `panel_data.csv`
- Interim tables: `panel_interim_<stage>.parquet`

### Logs and Summaries

- Run summaries: `logs/<stage>_summary.txt`
- Data record copies:
  - `logs/data_records/intake/<date>_<dataset>_intake.md`
  - `logs/data_records/analysis/<date>_<dataset>_analysis.md`
  - `logs/data_records/mapping/<date>_<dataset>_mapping.md`

## Traceability Requirements

Every deliverable result should be traceable to:

- the input dataset or processed table
- the script that produced it
- the relevant analysis or intake record when data changes were involved
- the date or run context used to generate it

If a result cannot be traced back, it is not ready for reporting.

## Result Summary Requirements

When reporting a new output, include:

- what was produced
- where it was saved
- which script produced it
- which input data it used
- key caveats or unresolved issues

Keep summaries concise, factual, and reproducible.

## Figure and Table Readiness

Before calling an output paper-ready, verify:

- the file is saved in the correct location
- the name follows the repository convention
- the content matches the intended specification
- the source data and script path are known

## Git and Review Notes

- Do not commit raw data files unless explicitly approved.
- Generated outputs should only be committed when they are intended project artifacts.
- When opening or updating a PR, summarize output-facing changes in user terms, not only file terms.
