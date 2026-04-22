# Data Intake Record

## Intake Metadata

| Field | Value |
| --- | --- |
| intake_id | 2026-04-16_cmcc_city_daily_emissions_batch_01 |
| dataset_name | CMCC 城市日度碳排放数据 |
| record_path | logs/data_records/intake/2026-04-16_cmcc_city_daily_emissions_intake.md |
| source_provider | 用户提供的 CMCC 原始 CSV |
| source_link | local file only; expected upstream family is Carbon Monitor China Cities / CMCC |
| access_method | user download and local placement |
| download_timestamp | 2026-04-16 |
| file_list | `data/raw/2026-04-13_统计建模数据/2019-2024 china_city_data_all.csv` |
| responsible_agent | Codex |

## Coverage and Grain

| Field | Value |
| --- | --- |
| geographic_grain | city (English city names; mixed China + non-China cities) |
| time_grain | daily |
| time_range | 2019-01-01 to 2025-04-30 |
| expected_primary_keys | `city + date + sector` |
| observed_primary_keys | `city + date + sector` |
| total_rows | 5,285,232 |
| total_columns | 4 |

## Definition and Unit Check

| Item | Value |
| --- | --- |
| key metric definitions captured | conditional |
| units documented | no |
| known source caveats | 文件名写作 `2019-2024`，但实际覆盖到 `2025-04-30`；字段仅有 `city/date/sector/value`，没有国家字段和城市代码；数据中混有明显非中国城市；需要后续核实 `value` 的精确单位和方法说明。 |

## Initial Quality Snapshot

| Check | Result | Notes |
| --- | --- | --- |
| duplicate key check | pass | 结构上表现为完整的 `city + date + sector` 日度网格；后续清洗时仍需程序化复核 |
| obvious type issues | conditional | `city/date/sector` 为字符串，`value` 为浮点；字段类型可读，但缺乏代码和国家标识 |
| out-of-range years | fail | 实际包含 2025 年，超出文件名标示的 2019-2024 |
| file integrity/readability | pass | CSV 可正常读取，MD5=`be5cffe6e65e34439a03b4247629de82` |

## Acceptance Decision

| Field | Value |
| --- | --- |
| intake_status | conditional |
| blocking_issues | 缺少国家字段与城市代码；与 PKU 城市名单仅部分英文名直接重合；精确单位和方法说明尚未随文件一并提供 |
| required_followups | 1. 构建中国城市筛选规则；2. 建立 CMCC 英文名到 PKU `pref_name_year18_eng`/城市代码映射表；3. 核实 `value` 单位与方法说明；4. 明确 2025 截断年是否完全剔除 |
| next_action_owner | Codex |
| decision_timestamp | 2026-04-16 |
