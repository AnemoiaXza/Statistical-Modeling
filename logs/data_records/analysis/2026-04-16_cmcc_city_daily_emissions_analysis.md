# Data Analysis Record

## Analysis Metadata

| Field | Value |
| --- | --- |
| analysis_id | 2026-04-16_cmcc_city_daily_emissions_batch_01 |
| dataset_or_panel_name | CMCC 城市日度碳排放数据 |
| record_path | logs/data_records/analysis/2026-04-16_cmcc_city_daily_emissions_analysis.md |
| producer_script_path | 终端抽样与全表统计（尚未形成正式 intake 脚本） |
| input_path | data/raw/2026-04-13_统计建模数据/2019-2024 china_city_data_all.csv |
| output_candidate_path | data/interim/cmcc/cmcc_annual_total_emissions_matched_candidates.csv |
| analysis_timestamp | 2026-04-16 |
| analyst | Codex |

## Descriptive Profile

| Metric | Value |
| --- | --- |
| row_count | 5,285,232 |
| column_count | 4 |
| city_count | 381 |
| year_range | 2019-2025 |
| key columns checked | `city`, `date`, `sector`, `value` |

## Missingness Summary

| Variable | Missing Count | Missing Rate | Action Note |
| --- | --- | --- | --- |
| `city` | 0 | 0% | 可直接读取，但需后续做中国城市筛选与英文名映射 |
| `date` | 0 | 0% | 可直接转为 `year` |
| `sector` | 0 | 0% | 共 6 个行业，含 `Total` |
| `value` | 0 | 0% | `Total` 行没有缺失，且未发现负值 |

## Anomaly Summary

| Variable | Rule/Method | Anomaly Count | Handling Note |
| --- | --- | --- | --- |
| `city` | 与 PKU `pref_name_year18_eng` 建立直接+标准化+人工别名匹配候选 | 46 个 unmatched，0 个 ambiguous | 已生成高置信自动映射，可直接形成 334 城年度候选面板；剩余 unmatched 仍需人工审阅 |
| `city` | 明显外国城市名单筛查 | 至少 25 个 | 说明该文件不是纯中国城市数据，需要先筛出中国城市 |
| `date` | 文件名 vs 实际年份范围核对 | 1 类 | 文件名写作 `2019-2024`，实际含 `2025-04-30` 截断数据 |
| `sector` | 唯一值核对 | 0 | `Aviation / Ground Transport / Industry / Power / Residential / Total` 结构完整 |

## Sample Change Log

| Stage | Rows | Cities | Years | Change Reason |
| --- | --- | --- | --- | --- |
| raw | 5,285,232 | 381 | 2019-2025 | 用户导入后的原始状态 |
| interim | n/a | n/a | n/a | 尚未进行中国城市筛选和年度汇总 |
| processed_candidate | n/a | n/a | n/a | 尚未形成可并表的城市年度排放表 |

## Risk and Follow-up

| Risk | Severity | Impact | Follow-up Action |
| --- | --- | --- | --- |
| 文件混有非中国城市 | high | 不能直接作为中国地级市面板结果变量源 | 先建立中国城市保留名单 |
| CMCC 英文城市名与 PKU 英文名只直接重合 270 个 | high | 无法直接按城市名并表，可能造成大样本损失 | 建立标准化映射表，处理拼写、空格、民族自治州/盟市等差异 |
| 文件含 2025 截断年 | medium | 若误入主样本，会破坏年度可比性 | 主样本先限制到 2019-2024 或 2019-2023 |
| `value` 单位未随文件附带说明 | medium | 影响论文口径表述与图表标注 | 补查上游说明页或论文附录 |

## Stage Conclusion

| Field | Value |
| --- | --- |
| ready_for_processed_handoff | no |
| unresolved_items | 中国城市筛选；CMCC-PKU 城市名映射；单位说明；是否纳入 2024/剔除 2025 |
| escalation_needed | no |
| notes | 从数据结构上看，该文件非常适合作为城市年化碳排放的原始底表，但前提是先完成城市筛选、命名映射和年度聚合。已生成 `data/interim/cmcc/cmcc_pku_city_match_candidates.csv`、`data/interim/cmcc/cmcc_annual_total_emissions.csv`、`data/interim/cmcc/cmcc_annual_total_emissions_matched_candidates.csv` 和 `data/interim/cmcc/cmcc_annual_total_emissions_resolved.csv`。当前匹配状态为 direct=263、normalized_candidate=39、manual_alias=34、unmatched=45；resolved 年度候选面板覆盖 334 城 × 2019-2024，共 2004 行。进一步与 PKU 2019-2023 面板合并后，已覆盖 327/338 个 PKU 城市，剩余缺口见 `logs/cmcc_pku_gap_report_2019_2023.txt`。 |
