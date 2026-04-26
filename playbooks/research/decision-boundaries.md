# Research Decision Boundaries

## Purpose

This playbook defines which decisions agents must not make without explicit user approval.
Use it whenever a task touches variable definitions, sample policy, model design, or interpretation.

For execution-only data handling, return to `playbooks/data/data-workflow.md`.

## Default Rule

If a choice changes the research design, the paper narrative, or the meaning of a reported result, stop and ask the user.

## Must Ask Before Proceeding

### Variable Definition Changes

Stop and ask before:

- replacing a planned variable with a proxy or alternative metric
- redefining an existing variable's unit, construction rule, or aggregation method
- switching the preferred digital economy measure to a backup measure
- switching the primary outcome from carbon efficiency to another outcome outside an approved robustness check

### Sample and Data Policy Changes

Stop and ask before:

- dropping cities or years beyond pre-agreed cleaning rules
- changing balanced-panel requirements
- altering missing-data handling rules beyond previously approved defaults
- accepting a dataset with coverage gaps that threaten the project time span

### DEA and Outcome Construction

Stop and ask before:

- changing DEA input variables
- changing DEA desired or undesired outputs
- substituting unavailable energy or capital measures with new proxies
- altering the efficiency model definition in a way that changes interpretation

### Model and Identification Design

Stop and ask before:

- adding or removing control variables in the main design
- changing the baseline causal estimator
- changing DML learner families in a way that alters the stated identification strategy
- changing treatment timing, panel structure, or identification window

### Heterogeneity and Robustness Design

Stop and ask before:

- redefining regional groups or subgroup boundaries
- changing heterogeneity features used for interpretation
- adding, removing, or replacing major robustness strategies
- turning an exploratory analysis into a headline result

### Result Interpretation and Reporting

Stop and ask before:

- writing causal claims stronger than the approved design supports
- treating a robustness result as the new main specification
- omitting material data limitations from a result summary

## Safe To Decide Without Asking

Agents may decide without asking when the change is purely executional and does not alter research meaning, for example:

- file naming within approved conventions
- log formatting
- script refactoring without behavior change
- adding non-controversial validation checks
- clarifying documentation wording without changing policy

## Escalation Format

When stopping to ask, report:

1. the exact decision point
2. why it matters for research design
3. the feasible options
4. the trade-off or risk of each option
5. the current recommendation, if one exists

Do not silently choose an option and continue.
