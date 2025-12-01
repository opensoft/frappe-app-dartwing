# Offline & Real-Time Sync Specification

**Objective:** Define deterministic sync behavior for Flutter clients (mobile/web/desktop) with Frappe backend.

## Goals

- Safe offline writes with predictable conflict handling.
- Bounded payloads via deltas and pagination.
- Org-scoped access enforced identically across REST, Socket.IO, and jobs.

## Data + API Shape

- Change feed endpoint: `/api/method/dartwing_core.sync.feed`
  - Params: `doctype`, `since` (timestamp or watermark), `limit`, `org`.
  - Returns: `{rows: [...], next_since, has_more}` where rows include `name`, `modified`, `docstatus`, `data`, `deleted` flag.
- Write queue endpoint: `/api/method/dartwing_core.sync.upsert_batch`
  - Payload: list of `{doctype, name?, data, client_ts, op}`; `op` in {insert, update, delete}.
  - Server responds with `{status, server_ts, resolved_doc}` per item.
- Socket.IO channel: `sync:<doctype>:<org>` emits deltas with same shape as feed rows.

## Conflict Strategy

### 1. AI Smart Merge (Primary)

- **Trigger:** When a conflict is detected (server `modified` > client `modified` and values differ).
- **Mechanism:**
  - Server sends `409 Conflict` with `server_doc` and `client_doc`.
  - Client (or Server, if online-only) invokes LLM: "Merge these two JSON objects representing a [Doctype]. Prioritize the most meaningful content. If unsure, return null."
  - **Success:** LLM returns merged JSON. Client submits merged version with `force=True`.
  - **Failure:** LLM returns null or low confidence score. Fallback to Human Resolution.

### 2. Human Fallback (Secondary)

- **Trigger:** AI Merge fails or is disabled for sensitive doctypes.
- **UI Workflow:**
  - App displays "Sync Conflict" banner.
  - User opens **Conflict Resolution Screen**:
    - **Side-by-Side Diff:** "Server Version" vs "Your Version".
    - **Field-Level Picker:** User taps to select which value to keep for each conflicting field.
    - **Manual Edit:** User can type a completely new value.
  - **Resolution:** User clicks "Resolve". Client submits final payload with `force=True`.

### 3. Last-Write-Wins (Audit Only)

- **Trigger:** Low-value, high-velocity data (e.g., "Last Seen" timestamp) where conflicts don't matter.
- **Mechanism:** Server accepts latest timestamp blindly but logs the overwrite in `Version` history.
- **Deletes:** Tombstones (`deleted=true`) always win over updates unless the update is a "Undelete" action.

## Per-DocType Conflict Strategies

Each DocType is assigned a default conflict strategy. This table defines the rules:

| DocType | Strategy | Server Wins | Client Wins | Notes |
|---------|----------|-------------|-------------|-------|
| Organization | `server_wins` | all fields | - | Authoritative org data |
| Person | `server_wins` | all fields | - | Identity data must be consistent |
| Org Member | `server_wins` | all fields | - | Membership is server-managed |
| Task | `field_level` | status, assigned_to, priority | notes, description | Collaborative editing |
| Calendar Event | `manual_resolve` | - | - | Time conflicts require human decision |
| Notification | `client_wins` | - | read_state, dismissed | Read state is user-local |
| Comment | `append_only` | - | - | Comments are immutable once created |
| File | `server_wins` | all fields | - | File metadata is authoritative |
| Equipment | `field_level` | assigned_to, current_location | notes | Location is server-tracked |
| _default | `server_wins` | all fields | - | Fallback for unlisted DocTypes |

### Strategy Definitions

| Strategy | Behavior |
|----------|----------|
| `server_wins` | Server version always takes precedence. Client changes discarded with notification. |
| `client_wins` | Client version takes precedence. Server updated to match client. |
| `field_level` | Merge at field level: use Server Wins/Client Wins lists to determine per-field winner. Unlisted fields default to server. |
| `manual_resolve` | Always show conflict resolution UI. No automatic merge. |
| `append_only` | Items can only be added, never modified. Deletes create tombstones. Concurrent additions merged as union. |
| `last_write_wins` | Most recent `modified` timestamp wins. No conflict UI shown. Logged for audit. |

### Implementation

```python
# dartwing_core/sync/conflict_strategies.py

CONFLICT_STRATEGIES = {
    "Organization": {
        "strategy": "server_wins",
    },
    "Person": {
        "strategy": "server_wins",
    },
    "Org Member": {
        "strategy": "server_wins",
    },
    "Task": {
        "strategy": "field_level",
        "server_wins_fields": ["status", "assigned_to", "priority", "due_date"],
        "client_wins_fields": ["notes", "description"],
    },
    "Calendar Event": {
        "strategy": "manual_resolve",
        "auto_merge_fields": ["notes"],  # These can merge even in manual mode
    },
    "Notification": {
        "strategy": "client_wins",
    },
    "Comment": {
        "strategy": "append_only",
    },
    "Equipment": {
        "strategy": "field_level",
        "server_wins_fields": ["assigned_to", "current_location", "status"],
        "client_wins_fields": ["notes"],
    },
    "_default": {
        "strategy": "server_wins",
    },
}


def get_conflict_strategy(doctype: str) -> dict:
    """Get conflict resolution strategy for a DocType."""
    return CONFLICT_STRATEGIES.get(doctype, CONFLICT_STRATEGIES["_default"])
```

### Adding New DocTypes

When creating a new DocType, add its conflict strategy to the table above and `CONFLICT_STRATEGIES` dict. Consider:

1. **Is the data authoritative on server?** → `server_wins`
2. **Is the data user-local (preferences, read state)?** → `client_wins`
3. **Is this collaborative with distinct field ownership?** → `field_level`
4. **Do conflicts require human judgment (scheduling, approvals)?** → `manual_resolve`
5. **Is this append-only data (logs, comments)?** → `append_only`

## Pagination & Backoff

- Default `limit` 100; cap at 500. Include `has_more` + `next_since` to continue.
- Clients apply exponential backoff on 5xx or network errors; stop after N attempts and surface to user/log.
- Delta retention: keep change log for 30 days; clients falling behind must trigger full resync for affected doctypes.

## Client Responsibilities

- Maintain local queue with durable storage; tag items with `client_ts`.
- Replay writes in order; handle 409 by surfacing conflict UI or deferring.
- Apply incoming deltas idempotently; ignore older than local `modified` unless conflict flow requires merge UI.
- Attachments: upload first, then send metadata record with file reference; server validates file presence.

## Permission Enforcement

- All feed and upsert calls must enforce `User Permission` scoped to Organization and concrete doctypes (`user_permission_doctypes`).
- Socket channels must verify org membership before subscribing; drop connection on role/org change.
- Background jobs emitting deltas must reuse shared permission utility to avoid leakage.

## Observability

- Metrics: queue depth, conflict rate, 5xx rate, average delta size, lag (`now - next_since`).
- Logs: per-request trace ID; include org + doctype for audit; error logs for rejected upserts with reason.
- Alerts: spike in conflicts, sustained lag > 5 minutes, failure to advance `next_since`.

## Test Matrix (minimum)

- Offline create/update/delete, replay with success.
- Conflict: client updates stale record → server LWW override recorded; conflict surfaced.
- Permission: user switched org loses feed access; socket unsubscribed.
- Large dataset: pagination continues until `has_more` false; attachments validated.
