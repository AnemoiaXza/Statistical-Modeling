# Data Intake Template

Use this template for each new dataset batch.

## Intake Metadata

| Field | Value |
| --- | --- |
| intake_id | |
| dataset_name | |
| source_provider | |
| source_link | |
| access_method | |
| download_timestamp | |
| file_list | |
| responsible_agent | |

## Coverage and Grain

| Field | Value |
| --- | --- |
| geographic_grain | |
| time_grain | |
| time_range | |
| expected_primary_keys | |
| observed_primary_keys | |
| total_rows | |
| total_columns | |

## Definition and Unit Check

| Item | Value |
| --- | --- |
| key metric definitions captured | yes / no |
| units documented | yes / no |
| known source caveats | |

## Initial Quality Snapshot

| Check | Result | Notes |
| --- | --- | --- |
| duplicate key check | pass / fail | |
| obvious type issues | pass / fail | |
| out-of-range years | pass / fail | |
| file integrity/readability | pass / fail | |

## Acceptance Decision

| Field | Value |
| --- | --- |
| intake_status | accepted / conditional / rejected |
| blocking_issues | |
| required_followups | |
| next_action_owner | |
| decision_timestamp | |
