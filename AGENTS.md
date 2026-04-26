# AGENTS Navigation

## Project Mission

This repository supports a statistical modeling competition project with reproducible data engineering, analysis, and modeling delivery.
`AGENTS.md` is the routing entrypoint, while detailed procedures live under `playbooks/`.

## Roles

- User owns research design decisions and paper writing.
- Agent owns implementation work for data processing, analysis execution, and code/document delivery.

## Read-First Order

1. `AGENTS.md`
2. Relevant `playbooks/...` document for the current task
3. Active plan in `docs/plans/`
4. Related code/data directories

## Task Routing

| Task Type | Read This First |
| --- | --- |
| Data download, intake, acceptance | `playbooks/data/data-workflow.md` |
| Dataset intake record | `playbooks/data/data-intake-template.md` |
| Dataset analysis record | `playbooks/data/data-analysis-template.md` |
| Variable raw-to-standard mapping | `playbooks/data/variable-mapping-template.md` |
| Research decision boundaries | `playbooks/research/decision-boundaries.md` |
| Output naming and delivery standards | `playbooks/delivery/output-standards.md` |

## Stop And Ask Triggers

Stop and ask the user before deciding any research design item, including:

- variable replacement or metric redefinition
- adding or removing control variables
- city/year sample deletion rules beyond agreed defaults
- DEA input or output definition changes
- DML, heterogeneity, or robustness strategy changes

## Cross-Cutting Working Rules

- Treat `data/raw/` as read-only.
- Keep analysis outputs traceable to input data and scripts.
- Record data intake and analysis using the matching playbook templates.
- If a task spans data handling and result delivery, read both the data and delivery playbooks before acting.
- Do not embed detailed templates or checklists into `AGENTS.md`; keep it as navigation.
- If a routed playbook file is missing, stop and ask before inventing process details.
