# Database Schema

All tables live in the `zendesk` schema.

## tickets

Main table. One row per Zendesk ticket.

| Column | Type | Description |
|---|---|---|
| `id` | bigint | Zendesk ticket ID (primary key for merges) |
| `subject` | varchar | Ticket subject line |
| `raw_subject` | varchar | Original subject before Zendesk processing |
| `description` | varchar | Full ticket description / first comment |
| `status` | varchar | `new`, `open`, `pending`, `hold`, `solved`, `closed` |
| `type` | varchar | `problem`, `incident`, `question`, `task` |
| `priority` | varchar | `urgent`, `high`, `normal`, `low` |
| `recipient` | varchar | Original recipient email address |
| `requester_id` | bigint | User ID of the requester |
| `submitter_id` | bigint | User ID of the submitter |
| `assignee_id` | bigint | User ID of the assigned agent |
| `organization_id` | bigint | Organization the requester belongs to |
| `group_id` | bigint | Agent group assigned to the ticket |
| `brand_id` | bigint | Brand associated with the ticket |
| `ticket_form_id` | bigint | Ticket form used |
| `custom_status_id` | bigint | Custom status identifier |
| `external_id` | varchar | External system reference |
| `url` | varchar | Zendesk API URL for this ticket |
| `created_at` | timestamptz | When the ticket was created |
| `updated_at` | timestamptz | When the ticket was last updated |
| `generated_timestamp` | bigint | Unix timestamp used for incremental sync |
| `has_incidents` | boolean | Whether the ticket has linked incidents |
| `is_public` | boolean | Whether the ticket has public comments |
| `allow_channelback` | boolean | Channel-back enabled |
| `allow_attachments` | boolean | Attachments allowed |
| `from_messaging_channel` | boolean | Originated from messaging |
| `tags` | varchar | Tags (stored as text; see `tickets__tags` for normalized form) |
| `custom_fields` | json | Custom field values as JSON |
| `satisfaction_rating__score` | varchar | CSAT score |
| `satisfaction_rating__id` | bigint | CSAT rating ID |
| `satisfaction_rating__reason` | varchar | CSAT reason text |
| `satisfaction_rating__reason_id` | bigint | CSAT reason ID |
| `satisfaction_rating__comment` | varchar | CSAT comment |
| `via__channel` | varchar | Channel the ticket came through |
| `via__source__from` | json | Source origin details |
| `via__source__to` | json | Source destination details |
| `via__source__rel` | varchar | Source relationship |
| `_dlt_load_id` | varchar | dlt load identifier |
| `_dlt_id` | varchar | dlt row identifier (unique) |

Custom fields specific to this Zendesk instance: `support_type`, `bugwash`, `waiting_for_release`, `do_not_auto_close`, `severity_level`, `product`, `git_hub_url`, `time_spent_last_update_secx`, `total_time_spent_secx`, `reason`.

## tickets__tags

One row per tag per ticket.

| Column | Type | Description |
|---|---|---|
| `value` | varchar | Tag name |
| `_dlt_root_id` | varchar | References `tickets._dlt_id` |
| `_dlt_parent_id` | varchar | Parent record ID |
| `_dlt_list_idx` | bigint | Position in the tags array |
| `_dlt_id` | varchar | Row identifier (unique) |

## tickets__collaborator_ids

One row per collaborator per ticket.

| Column | Type | Description |
|---|---|---|
| `value` | bigint | Zendesk user ID of the collaborator |
| `_dlt_root_id` | varchar | References `tickets._dlt_id` |
| `_dlt_parent_id` | varchar | Parent record ID |
| `_dlt_list_idx` | bigint | Position in the array |
| `_dlt_id` | varchar | Row identifier (unique) |

## tickets__follower_ids

Same structure as `tickets__collaborator_ids`. Contains user IDs of ticket followers.

## tickets__email_cc_ids

Same structure as `tickets__collaborator_ids`. Contains user IDs of email CC recipients.

## tickets__followup_ids

Same structure as `tickets__collaborator_ids`. Contains ticket IDs of follow-up tickets.

## Joining child tables

All child tables join to `tickets` via `_dlt_root_id`:

```sql
SELECT t.id, t.subject, tag.value AS tag
FROM zendesk.tickets t
JOIN zendesk.tickets__tags tag ON tag._dlt_root_id = t._dlt_id
WHERE tag.value = 'varnish_enterprise';
```

## dlt internal tables

- `_dlt_loads` — load tracking
- `_dlt_version` — schema version history
- `_dlt_pipeline_state` — incremental sync state (last sync timestamp)
