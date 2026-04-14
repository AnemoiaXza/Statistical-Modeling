# Policy Text Corpus Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Build a reproducible policy-text corpus pipeline that discovers, stores, normalizes, deduplicates, scores, validates, and aggregates 2020-2024 double-carbon policy documents into a `city-year` panel for mechanism and moderation analysis.

**Architecture:** Keep numbered scripts as thin entrypoints and place reusable logic in a new `src/stat_modeling/policy_text/` package. The first implementation batch should separate corpus assembly from LLM scoring so downloads, normalization, and rule features remain reproducible even if the scoring backend changes later.

**Tech Stack:** Python, pandas, requests, beautifulsoup4, pypdf or pdfplumber, pytest, existing `stat_modeling` package utilities

---

### Task 1: Add policy-text paths and package skeleton

**Files:**
- Modify: `src/stat_modeling/config.py`
- Create: `src/stat_modeling/policy_text/__init__.py`
- Create: `tests/test_policy_text_config.py`

**Step 1: Write the failing test**

```python
from stat_modeling.config import POLICY_TEXT_INTERIM_DIR
from stat_modeling.config import POLICY_TEXT_PROCESSED_DIR
from stat_modeling.config import POLICY_TEXT_LOGS_DIR
from stat_modeling.config import ensure_project_directories


def test_policy_text_directories_are_created(tmp_path, monkeypatch):
    monkeypatch.setattr("stat_modeling.config.INTERIM_DATA_DIR", tmp_path / "interim")
    monkeypatch.setattr("stat_modeling.config.PROCESSED_DATA_DIR", tmp_path / "processed")
    monkeypatch.setattr("stat_modeling.config.LOGS_DIR", tmp_path / "logs")

    created = ensure_project_directories()

    assert any(path.name == "policy_text" for path in created)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_config.py -v`
Expected: FAIL because policy-text paths do not exist in `config.py`.

**Step 3: Write minimal implementation**

```python
POLICY_TEXT_INTERIM_DIR = INTERIM_DATA_DIR / "policy_text"
POLICY_TEXT_PROCESSED_DIR = PROCESSED_DATA_DIR / "policy_text"
POLICY_TEXT_LOGS_DIR = LOGS_DIR / "policy_text"

REQUIRED_DIRECTORIES = (
    ...,
    POLICY_TEXT_INTERIM_DIR,
    POLICY_TEXT_PROCESSED_DIR,
    POLICY_TEXT_LOGS_DIR,
)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_policy_text_config.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/config.py src/stat_modeling/policy_text/__init__.py tests/test_policy_text_config.py
git commit -m "feat: add policy text workspace paths"
```

### Task 2: Implement metadata model and storage conventions

**Files:**
- Create: `src/stat_modeling/policy_text/models.py`
- Create: `src/stat_modeling/policy_text/storage.py`
- Create: `tests/test_policy_text_models.py`

**Step 1: Write the failing test**

```python
from stat_modeling.policy_text.models import PolicyDocument


def test_policy_document_normalizes_required_fields():
    document = PolicyDocument(
        title="关于推进节能降碳行动的通知",
        pub_date="2024-05-29",
        issuing_body="国务院",
        admin_level="central",
        region_name="China",
        source_url="https://www.gov.cn/example",
        content_text="全文内容",
    )

    assert document.doc_id.startswith("central_2024")
    assert document.doc_no is None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_models.py -v`
Expected: FAIL because `PolicyDocument` is undefined.

**Step 3: Write minimal implementation**

```python
from dataclasses import dataclass


@dataclass(slots=True)
class PolicyDocument:
    title: str
    pub_date: str
    issuing_body: str
    admin_level: str
    region_name: str
    source_url: str
    content_text: str
    doc_no: str | None = None

    @property
    def doc_id(self) -> str:
        return f"{self.admin_level}_{self.pub_date}_{abs(hash((self.title, self.issuing_body)))}"
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_policy_text_models.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/policy_text/models.py src/stat_modeling/policy_text/storage.py tests/test_policy_text_models.py
git commit -m "feat: add policy text document model"
```

### Task 3: Build source registry and discovery layer

**Files:**
- Create: `src/stat_modeling/policy_text/discovery.py`
- Create: `tests/test_policy_text_discovery.py`

**Step 1: Write the failing test**

```python
from stat_modeling.policy_text.discovery import build_keyword_query
from stat_modeling.policy_text.discovery import select_supported_source


def test_build_keyword_query_includes_green_and_carbon_terms():
    query = build_keyword_query(year=2024)
    assert "碳达峰" in query
    assert "数字化绿色转型" in query


def test_select_supported_source_for_gov():
    source = select_supported_source("https://www.gov.cn/zhengce")
    assert source.source_site == "gov.cn"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_discovery.py -v`
Expected: FAIL because discovery helpers do not exist.

**Step 3: Write minimal implementation**

```python
KEY_TERMS = (
    "双碳",
    "碳达峰",
    "碳中和",
    "节能降碳",
    "绿色低碳",
    "数字绿色融合",
    "数字化绿色转型",
)


def build_keyword_query(year: int) -> str:
    return f"{year} " + " OR ".join(KEY_TERMS)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_policy_text_discovery.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/policy_text/discovery.py tests/test_policy_text_discovery.py
git commit -m "feat: add policy text source discovery registry"
```

### Task 4: Implement fetch, normalization, and raw capture

**Files:**
- Create: `src/stat_modeling/policy_text/fetch.py`
- Create: `src/stat_modeling/policy_text/normalize.py`
- Create: `tests/test_policy_text_normalize.py`

**Step 1: Write the failing test**

```python
from stat_modeling.policy_text.normalize import normalize_policy_record


def test_normalize_policy_record_extracts_core_fields():
    raw_record = {
        "title": "上海市加快建立产品碳足迹管理体系行动方案",
        "pub_date": "2024-03-25",
        "issuing_body": "上海市人民政府",
        "source_url": "https://www.shanghai.gov.cn/example",
        "content_text": "提出目标、责任单位和实施期限。",
    }

    normalized = normalize_policy_record(raw_record, admin_level="municipal", region_name="上海市")

    assert normalized["admin_level"] == "municipal"
    assert normalized["region_name"] == "上海市"
    assert normalized["content_text"].startswith("提出目标")
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_normalize.py -v`
Expected: FAIL because normalization helpers are missing.

**Step 3: Write minimal implementation**

```python
def normalize_policy_record(raw_record: dict[str, str], admin_level: str, region_name: str) -> dict[str, str]:
    return {
        "title": raw_record["title"].strip(),
        "pub_date": raw_record["pub_date"],
        "issuing_body": raw_record["issuing_body"].strip(),
        "admin_level": admin_level,
        "region_name": region_name,
        "source_url": raw_record["source_url"],
        "content_text": raw_record["content_text"].strip(),
    }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_policy_text_normalize.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/policy_text/fetch.py src/stat_modeling/policy_text/normalize.py tests/test_policy_text_normalize.py
git commit -m "feat: add policy text normalization pipeline"
```

### Task 5: Implement deduplication and document-status tracking

**Files:**
- Create: `src/stat_modeling/policy_text/dedupe.py`
- Create: `tests/test_policy_text_dedupe.py`

**Step 1: Write the failing test**

```python
import pandas as pd

from stat_modeling.policy_text.dedupe import deduplicate_policy_records


def test_deduplicate_prefers_formal_publication():
    frame = pd.DataFrame(
        [
            {"title": "通知", "pub_date": "2024-01-01", "issuing_body": "国务院", "doc_no": "国发1号", "is_official": False},
            {"title": "通知", "pub_date": "2024-01-01", "issuing_body": "国务院", "doc_no": "国发1号", "is_official": True},
        ]
    )

    result = deduplicate_policy_records(frame)

    assert len(result) == 1
    assert bool(result.iloc[0]["is_official"]) is True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_dedupe.py -v`
Expected: FAIL because dedupe logic is missing.

**Step 3: Write minimal implementation**

```python
def deduplicate_policy_records(frame: pd.DataFrame) -> pd.DataFrame:
    ordered = frame.sort_values(["doc_no", "is_official"], ascending=[True, False])
    return ordered.drop_duplicates(subset=["doc_no"], keep="first").reset_index(drop=True)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_policy_text_dedupe.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/policy_text/dedupe.py tests/test_policy_text_dedupe.py
git commit -m "feat: add policy text deduplication rules"
```

### Task 6: Implement rule-based feature extraction

**Files:**
- Create: `src/stat_modeling/policy_text/rules.py`
- Create: `tests/test_policy_text_rules.py`

**Step 1: Write the failing test**

```python
from stat_modeling.policy_text.rules import extract_rule_features


def test_extract_rule_features_detects_targets_deadlines_and_digital_terms():
    text = "到2025年实现单位能耗下降3%，由市发展改革委牵头，建立年度考核机制，推进数字化绿色转型。"

    features = extract_rule_features(text)

    assert features["has_quant_target"] is True
    assert features["has_deadline"] is True
    assert features["has_responsibility"] is True
    assert features["has_assessment"] is True
    assert features["has_digital_term"] is True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_rules.py -v`
Expected: FAIL because rule extractor is undefined.

**Step 3: Write minimal implementation**

```python
def extract_rule_features(text: str) -> dict[str, bool]:
    return {
        "has_quant_target": "%" in text or "目标" in text,
        "has_deadline": "到202" in text or "期限" in text,
        "has_responsibility": "负责" in text or "牵头" in text,
        "has_assessment": "考核" in text or "问责" in text or "监督" in text,
        "has_digital_term": "数字" in text or "数据" in text or "智能" in text or "平台" in text,
    }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_policy_text_rules.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/policy_text/rules.py tests/test_policy_text_rules.py
git commit -m "feat: add policy text rule features"
```

### Task 7: Implement LLM scoring schema and batch preparation

**Files:**
- Create: `src/stat_modeling/policy_text/llm_schema.py`
- Create: `tests/test_policy_text_llm_schema.py`

**Step 1: Write the failing test**

```python
from stat_modeling.policy_text.llm_schema import build_scoring_payload


def test_build_scoring_payload_contains_three_scores_and_document_context():
    payload = build_scoring_payload(
        title="关于加快绿色低碳转型的意见",
        content_text="明确提出责任分工、量化指标和数字平台建设要求。",
    )

    assert "policy_strength" in payload["schema"]["properties"]
    assert "execution_clarity" in payload["schema"]["properties"]
    assert "digital_green_synergy" in payload["schema"]["properties"]
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_llm_schema.py -v`
Expected: FAIL because LLM schema helpers do not exist.

**Step 3: Write minimal implementation**

```python
def build_scoring_payload(title: str, content_text: str) -> dict[str, object]:
    return {
        "document": {"title": title, "content_text": content_text},
        "schema": {
            "type": "object",
            "properties": {
                "policy_strength": {"type": "number"},
                "execution_clarity": {"type": "number"},
                "digital_green_synergy": {"type": "number"},
            },
            "required": ["policy_strength", "execution_clarity", "digital_green_synergy"],
        },
    }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_policy_text_llm_schema.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/policy_text/llm_schema.py tests/test_policy_text_llm_schema.py
git commit -m "feat: add policy text llm scoring schema"
```

### Task 8: Implement city-year assignment and aggregation

**Files:**
- Create: `src/stat_modeling/policy_text/aggregate.py`
- Create: `tests/test_policy_text_aggregate.py`

**Step 1: Write the failing test**

```python
import pandas as pd

from stat_modeling.policy_text.aggregate import assign_documents_to_cities
from stat_modeling.policy_text.aggregate import aggregate_policy_scores


def test_assign_and_aggregate_policy_scores():
    documents = pd.DataFrame(
        [
            {"admin_level": "central", "region_name": "China", "pub_date": "2024-01-01", "policy_strength": 3.0, "execution_clarity": 4.0, "digital_green_synergy": 5.0},
            {"admin_level": "provincial", "region_name": "浙江省", "pub_date": "2024-02-01", "policy_strength": 2.0, "execution_clarity": 3.0, "digital_green_synergy": 4.0},
        ]
    )
    cities = pd.DataFrame(
        [
            {"city_name_cn": "杭州市", "province_name_cn": "浙江省", "year": 2024},
            {"city_name_cn": "广州市", "province_name_cn": "广东省", "year": 2024},
        ]
    )

    assigned = assign_documents_to_cities(documents, cities)
    aggregated = aggregate_policy_scores(assigned)

    hangzhou = aggregated.loc[aggregated["city_name_cn"] == "杭州市"].iloc[0]
    assert hangzhou["sum_policy_strength_city_year"] == 5.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_aggregate.py -v`
Expected: FAIL because aggregation helpers are missing.

**Step 3: Write minimal implementation**

```python
def assign_documents_to_cities(documents: pd.DataFrame, cities: pd.DataFrame) -> pd.DataFrame:
    # central -> all cities; provincial -> province match; municipal -> city match
    ...


def aggregate_policy_scores(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.groupby(["city_name_cn", "year"], as_index=False).agg(
        sum_policy_strength_city_year=("policy_strength", "sum"),
        mean_policy_strength_city_year=("policy_strength", "mean"),
    )
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_policy_text_aggregate.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/policy_text/aggregate.py tests/test_policy_text_aggregate.py
git commit -m "feat: add policy text city year aggregation"
```

### Task 9: Implement validation helpers

**Files:**
- Create: `src/stat_modeling/policy_text/validation.py`
- Create: `tests/test_policy_text_validation.py`

**Step 1: Write the failing test**

```python
import pandas as pd

from stat_modeling.policy_text.validation import summarize_score_alignment


def test_summarize_score_alignment_reports_rule_llm_directions():
    frame = pd.DataFrame(
        [
            {"has_quant_target": True, "policy_strength": 4.5},
            {"has_quant_target": False, "policy_strength": 1.0},
        ]
    )

    summary = summarize_score_alignment(frame)

    assert "policy_strength_by_quant_target" in summary
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_validation.py -v`
Expected: FAIL because validation helpers are missing.

**Step 3: Write minimal implementation**

```python
def summarize_score_alignment(frame: pd.DataFrame) -> dict[str, float]:
    grouped = frame.groupby("has_quant_target")["policy_strength"].mean().to_dict()
    return {"policy_strength_by_quant_target": grouped}
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_policy_text_validation.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/stat_modeling/policy_text/validation.py tests/test_policy_text_validation.py
git commit -m "feat: add policy text validation summaries"
```

### Task 10: Add CLI entrypoint and end-to-end smoke test

**Files:**
- Create: `src/08_policy_text.py`
- Create: `tests/test_policy_text_pipeline_smoke.py`
- Modify: `README.md`
- Modify: `environment.yml`

**Step 1: Write the failing test**

```python
from pathlib import Path
from subprocess import run


def test_policy_text_script_runs_with_help():
    result = run(
        ["python3", "src/08_policy_text.py", "--help"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "usage" in result.stdout.lower()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_policy_text_pipeline_smoke.py -v`
Expected: FAIL because the CLI entrypoint does not exist.

**Step 3: Write minimal implementation**

```python
import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Policy text corpus pipeline.")
    parser.add_argument("--stage", choices=["discover", "normalize", "rules", "aggregate"], required=False)
    return parser
```

**Step 4: Run focused and full tests**

Run: `pytest tests/test_policy_text_pipeline_smoke.py -v`
Expected: PASS

Run: `pytest tests/test_policy_text_*.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/08_policy_text.py README.md environment.yml tests/test_policy_text_pipeline_smoke.py
git commit -m "feat: add policy text pipeline cli"
```

### Task 11: Run full verification and produce handoff notes

**Files:**
- Modify: `README.md`
- Modify: `docs/plans/2026-04-14-policy-text-corpus-design.md`
- Create: `logs/policy_text/implementation_summary.txt`

**Step 1: Run the complete targeted suite**

Run: `pytest tests/test_policy_text_*.py tests/test_config.py tests/test_data_io.py -v`
Expected: PASS

**Step 2: Run the CLI smoke checks**

Run: `python3 src/08_policy_text.py --help`
Expected: prints usage and exits 0

**Step 3: Write handoff summary**

```text
Implemented policy-text corpus scaffold.
Verified config paths, discovery, normalization, dedupe, rules, LLM schema, aggregation, validation, and CLI help.
```

**Step 4: Commit**

```bash
git add README.md docs/plans/2026-04-14-policy-text-corpus-design.md logs/policy_text/implementation_summary.txt
git commit -m "docs: record policy text implementation handoff"
```
