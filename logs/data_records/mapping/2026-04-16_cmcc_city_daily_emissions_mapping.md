# Variable Mapping Record

## Mapping Metadata

| Field | Value |
| --- | --- |
| mapping_id | 2026-04-16_cmcc_city_daily_emissions_batch_01 |
| dataset_name | CMCC 城市日度碳排放数据 |
| record_path | logs/data_records/mapping/2026-04-16_cmcc_city_daily_emissions_mapping.md |
| source_path | data/raw/2026-04-13_统计建模数据/2019-2024 china_city_data_all.csv |
| prepared_by | Codex |
| prepared_timestamp | 2026-04-16 |

## Raw-to-Standard Mapping

| raw_dataset | raw_field | standard_variable | standard_description | raw_unit | standard_unit | transform_rule | key_role | coverage_note | quality_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `2019-2024 china_city_data_all.csv` | `city` | `city_name_en_raw` | 原始英文城市名 | text | text | 保留原值；后续建立与 `pref_name_year18_eng` 的标准化映射 | city_key | 381 个城市名 | 混有非中国城市，且与 PKU 英文名只部分直接匹配 |
| `2019-2024 china_city_data_all.csv` | `date` | `date` | 原始日期 | date | date | 保留原值；用于生成 `year` | time_key | 2019-01-01 至 2025-04-30 | 2025 为截断年 |
| `2019-2024 china_city_data_all.csv` | `date` | `year` | 年度键 | date | year | `year = to_datetime(date).year` | time_key | 2019-2025 | 主样本拟仅保留完整年度 |
| `2019-2024 china_city_data_all.csv` | `sector` | `emission_sector` | 排放行业维度 | category | category | 保留原值；常用 `Total` 作为年度总排放 | non-key | 6 类行业 | 包含 `Total`，适合直接聚合总量 |
| `2019-2024 china_city_data_all.csv` | `value` | `co2_emission_daily` | 城市-日-行业排放值 | unknown | pending verification | 先数值化；后续核实单位说明 | non-key | 无缺失 | 单位需补查上游说明 |
| `2019-2024 china_city_data_all.csv` | `value` with `sector == 'Total'` | `co2_emission_daily_total` | 城市日度总排放 | unknown | pending verification | 过滤 `sector == 'Total'` 后直接保留 | non-key | 381 城，2019-2025 | 适合作为年化总排放基础 |
| `2019-2024 china_city_data_all.csv` | `value` with `sector == 'Total'` grouped by `city, year` | `co2_emission` | 城市年度碳排放总量 | unknown | pending verification | 对 `Total` 行按 `city + year` 聚合求和；仅保留完整年度 | non-key | 候选主结果/稳健性结果分子 | 形成年度面板前必须先完成中国城市筛选和英文名映射 |

## Variable Gap Log

| expected_standard_variable | gap_type | note | planned_resolution |
| --- | --- | --- | --- |
| `city_code` | missing_source | 原始表无国家字段、无城市代码 | 已生成 `data/interim/cmcc/cmcc_pku_city_match_candidates.csv` 作为映射候选表，并生成 `data/interim/cmcc/cmcc_annual_total_emissions_resolved.csv` 将高置信匹配映射到 PKU `pref_code_year18` |
| `city_name_cn` | missing_source | 原始表仅有英文名 | 通过 PKU 英文名映射到中文名 |
| `country_flag` | missing_source | 无法直接区分中国与非中国城市 | 通过城市保留名单或 PKU 交叉映射筛出中国城市 |
| `co2_emission` standard_unit | unit_conflict | 文件未附带明确单位说明 | 补查 CMCC 上游数据说明或论文附录 |
| `2019-2023 balanced city panel` | definition_conflict | 原始日度表含 2025 截断年，且 381 城与 PKU 331 城口径不一 | 先限制完整年度，再以中国城市映射后的交集构建面板 |

## Sign-off

| Field | Value |
| --- | --- |
| mapping_status | draft |
| reviewer | pending |
| review_timestamp | pending |
| signoff_notes | 该记录确认了 CMCC 原始表可用于生成年度碳排放结果变量。当前已可稳定产出完整年度总排放表，并形成高置信 `334` 城的 resolved 候选面板；剩余 `46` 个 unmatched 城市仍需人工复核后才能决定是否进一步扩大样本。 |
