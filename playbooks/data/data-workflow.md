# Data Workflow

## Purpose

This playbook defines the data lifecycle for this project:
download -> intake -> acceptance -> analysis record -> processed handoff -> traceable outputs.

Use this workflow for every dataset batch before model code consumes it.

## Scope

- In scope: data handling, quality checks, analysis records, storage locations, and handoff artifacts.
- Out of scope: research design decisions (variable definition changes, model specification changes, sample policy changes).

## Required Locations

| Artifact | Required Location |
| --- | --- |
| Raw files (read-only) | `data/raw/` |
| Interim working tables | `data/interim/` |
| Accepted processed tables | `data/processed/` |
| Tables for reporting | `outputs/tables/` |
| Figures for reporting | `outputs/figures/` |
| Run summaries / logs | `logs/` |
| Intake record | `playbooks/data/data-intake-template.md` (copy to run record file) |
| Analysis record | `playbooks/data/data-analysis-template.md` (copy to run record file) |
| Field mapping record | `playbooks/data/variable-mapping-template.md` (copy to run record file) |

## Workflow Stages

### Stage 1: Download and Register

Inputs:
- Source link or provider
- Dataset version/date

Outputs:
- Raw files saved under `data/raw/`
- One intake record based on `data-intake-template.md`

Checks:
- File checksum or row count captured
- Source and coverage explicitly recorded

### Stage 2: Intake and Acceptance

Inputs:
- Raw files in `data/raw/`
- Intake record draft

Outputs:
- Completed intake record with pass/fail status
- Acceptance notes with known limitations

Checks:
- Key fields available (`city_code`, `year`, or documented equivalent)
- Coverage range recorded
- Units and definitions documented

### Stage 3: Variable Mapping

Inputs:
- Accepted raw dataset

Outputs:
- Field mapping record from raw names to standard project variables

Checks:
- Every modeling variable has a source field or an explicit gap
- Transform rules and units are documented per field

### Stage 4: Dataset Analysis Record

Inputs:
- Candidate table after initial harmonization

Outputs:
- Analysis record based on `data-analysis-template.md`

Checks:
- Descriptive profile captured
- Missingness and anomalies recorded
- Sample-size changes documented
- Risks and follow-up actions listed

### Stage 5: Processed Handoff

Inputs:
- Accepted cleaning outputs
- Analysis and mapping records

Outputs:
- Final tables in `data/processed/`
- Handoff summary in `logs/`

Checks:
- Outputs are reproducible from scripts
- Output file names follow repository conventions
- Traceability from output -> script -> input is preserved

## Stop Line

Stop execution and ask for confirmation when:
- required keys are missing and no equivalent key is available
- source coverage cannot meet project year range
- unit/definition conflicts block consistent mapping
- data quality issues make acceptance uncertain

Do not silently continue past these points.
