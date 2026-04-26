# Paper Draft Maintenance Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Create a maintainable paper draft workspace that keeps the title, abstract, keywords, and key decisions aligned with the evolving data/modeling pipeline.

**Architecture:** Use one main draft file for reader-facing narrative and one decision log for research governance. Keep both under `docs/paper/` so they version with the code/data pipeline and can be updated incrementally.

**Tech Stack:** Markdown, existing docs under `docs/plans/`, local repository conventions

---

### Task 1: Create paper draft directory and scaffold

**Files:**
- Create: `docs/paper/01_draft.md`
- Create: `docs/paper/decision-log.md`

**Step 1: Draft the paper main file**

Include:
- title
- abstract draft
- keywords
- current confirmed design
- current data/sample status
- current limitations

**Step 2: Draft the decision log**

Include:
- confirmed decisions
- unresolved decisions
- data/model/write-up impacts

**Step 3: Verify files exist and are readable**

Run:
`test -f docs/paper/01_draft.md && test -f docs/paper/decision-log.md`

Expected:
Both files exist.

### Task 2: Fill first-version content from current repo state

**Files:**
- Modify: `docs/paper/01_draft.md`
- Modify: `docs/paper/decision-log.md`

**Step 1: Sync confirmed research choices**

Source from:
- `docs/plans/2026-04-14-research-direction-and-literature-memo.md`
- `logs/modeling_candidate_coverage_report_2019_2023.txt`
- `logs/dml_input_readiness_summary.txt`

**Step 2: Mark unresolved boundaries clearly**

Must include:
- population control variable still candidate-only
- current ready sample is `294` cities / `1456` rows

**Step 3: Verify content is not stale**

Run:
`rg -n "294|1456|population_control_candidate|数字普惠金融" docs/paper/01_draft.md docs/paper/decision-log.md`

Expected:
Current values present in both files as appropriate.
