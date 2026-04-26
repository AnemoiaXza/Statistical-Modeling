# Agent Navigation and Playbooks Design

## Context

This repository needs a stable top-level navigation file for future agent work.
The user wants `AGENTS.md` to act as a map rather than a rule dump, while detailed execution requirements live in a separate `playbooks/` directory.

The immediate goal is to support a research workflow where data acquisition, data analysis, and result production are treated as first-class development activities, with explicit handoffs and records.

## Chosen Approach

Adopt a two-layer documentation system:

- `AGENTS.md` is the entrypoint and routing layer
- `playbooks/` contains durable workflow documents and templates

This keeps the top-level instructions short, reduces duplication, and makes it easier to evolve detailed process documents without rewriting the repository entrypoint.

## Documentation Architecture

```text
AGENTS.md
playbooks/
├── data/
│   ├── data-workflow.md
│   ├── data-intake-template.md
│   ├── data-analysis-template.md
│   └── variable-mapping-template.md
├── research/
│   └── decision-boundaries.md
└── delivery/
    └── output-standards.md
```

## AGENTS.md Scope

`AGENTS.md` should stay intentionally thin.
It should contain only the information an agent needs to orient itself and route to the correct playbook:

- project mission
- roles and decision ownership
- required reading order
- task-routing map
- stop-and-ask triggers
- cross-cutting working rules

It should not duplicate detailed templates, field definitions, or output formatting checklists that belong in playbooks.

## Playbook Responsibilities

### `playbooks/data/`

These documents define how agents handle data as an engineering and analysis workflow:

- `data-workflow.md`
  - end-to-end flow from download to accepted processed data
  - required records, checkpoints, and outputs
- `data-intake-template.md`
  - template for new dataset intake
  - source, coverage, unit, key, missingness, and usability summary
- `data-analysis-template.md`
  - template for dataset-level analysis
  - descriptive statistics, missingness, anomalies, sample changes, and conclusions
- `variable-mapping-template.md`
  - canonical raw-to-standard field mapping record

### `playbooks/research/`

- `decision-boundaries.md`
  - lists decisions agents must not make without user approval
  - especially variable substitution, deletion rules, model specification changes, and grouping design

### `playbooks/delivery/`

- `output-standards.md`
  - naming rules for tables, figures, logs, and result summaries
  - expectations for traceability from result back to script and input

## Reading and Routing Rules

Agents should read documents in this order:

1. `AGENTS.md`
2. the playbook matched to the task type
3. the current plan under `docs/plans/` if implementation is in progress
4. only then the relevant code or data directories

This ordering ensures agents understand repository norms before touching artifacts.

## Stop-and-Ask Boundary

The new documentation must keep research design decisions under human control.
Agents must stop and ask before deciding:

- whether to replace a variable definition
- whether to add or remove control variables
- whether to drop cities or years beyond pre-agreed rules
- whether to change DEA input or output definitions
- whether to alter heterogeneity group definitions
- whether to add or remove robustness strategies

## Non-Goals

This change should not:

- implement data ingestion code
- implement new modeling code
- duplicate the existing project design or bootstrap plans
- define irreversible research decisions that belong to the user
