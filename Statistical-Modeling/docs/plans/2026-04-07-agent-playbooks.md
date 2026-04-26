# Agent Navigation and Playbooks Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a lightweight `AGENTS.md` entrypoint plus `playbooks/` documents that route future agent work for data, research, and delivery tasks.

**Architecture:** Keep `AGENTS.md` as a navigation layer only, with all durable detail moved into `playbooks/data/`, `playbooks/research/`, and `playbooks/delivery/`. The work is documentation-first, so validation should focus on file existence, routing completeness, and consistency of cross-references rather than application code behavior.

**Tech Stack:** Markdown, git, shell validation commands.

---

### Task 1: Add AGENTS.md Navigation Layer

**Files:**
- Create: `AGENTS.md`

**Step 1: Write the failing validation**

Run: `test -f AGENTS.md`
Expected: exit code 1 because the file does not exist yet.

**Step 2: Create the minimal implementation**

Write `AGENTS.md` with:
- project mission
- user/agent role split
- read-first order
- task-routing table to `playbooks/`
- stop-and-ask triggers
- cross-cutting working rules

**Step 3: Run validation to verify it passes**

Run: `test -f AGENTS.md`
Expected: exit code 0

**Step 4: Commit**

```bash
git add AGENTS.md
git commit -m "docs: add agent navigation entrypoint"
```

### Task 2: Add Data Playbooks

**Files:**
- Create: `playbooks/data/data-workflow.md`
- Create: `playbooks/data/data-intake-template.md`
- Create: `playbooks/data/data-analysis-template.md`
- Create: `playbooks/data/variable-mapping-template.md`

**Step 1: Write the failing validation**

Run: `test -f playbooks/data/data-workflow.md`
Expected: exit code 1 because the directory and files do not exist yet.

**Step 2: Create the minimal implementation**

Write four data playbooks that cover:
- dataset download, intake, acceptance, and traceability
- dataset analysis records and stage conclusions
- raw-to-standard variable mapping
- explicit outputs and storage locations

**Step 3: Run validation to verify it passes**

Run: `test -f playbooks/data/data-workflow.md && test -f playbooks/data/data-intake-template.md && test -f playbooks/data/data-analysis-template.md && test -f playbooks/data/variable-mapping-template.md`
Expected: exit code 0

**Step 4: Commit**

```bash
git add playbooks/data
git commit -m "docs: add data workflow playbooks"
```

### Task 3: Add Research and Delivery Playbooks

**Files:**
- Create: `playbooks/research/decision-boundaries.md`
- Create: `playbooks/delivery/output-standards.md`

**Step 1: Write the failing validation**

Run: `test -f playbooks/research/decision-boundaries.md`
Expected: exit code 1 because the file does not exist yet.

**Step 2: Create the minimal implementation**

Write:
- a research decision boundary document listing which modeling and variable decisions require user approval
- an output standards document defining naming, traceability, and reporting expectations

**Step 3: Run validation to verify it passes**

Run: `test -f playbooks/research/decision-boundaries.md && test -f playbooks/delivery/output-standards.md`
Expected: exit code 0

**Step 4: Commit**

```bash
git add playbooks/research playbooks/delivery
git commit -m "docs: add research and delivery playbooks"
```

### Task 4: Verify Cross-References and Structure

**Files:**
- Modify: `AGENTS.md`
- Modify: `playbooks/data/data-workflow.md`
- Modify: `playbooks/research/decision-boundaries.md`
- Modify: `playbooks/delivery/output-standards.md`

**Step 1: Run structural validation**

Run: `find playbooks -maxdepth 2 -type f | sort`
Expected: shows exactly the planned playbook files.

**Step 2: Run routing validation**

Run: `rg -n "playbooks/" AGENTS.md`
Expected: confirms `AGENTS.md` routes tasks to the detailed playbooks.

**Step 3: Review consistency**

Check that:
- `AGENTS.md` does not duplicate detailed template content
- research stop-lines in `AGENTS.md` match `playbooks/research/decision-boundaries.md`
- data traceability requirements in `AGENTS.md` and `playbooks/data/data-workflow.md` are aligned
- output naming guidance is consistent with project naming conventions

**Step 4: Commit**

```bash
git add AGENTS.md playbooks
git commit -m "docs: verify agent playbook structure"
```
