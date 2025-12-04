# Offline Sync Resolution Plan

**Module:** dartwing_company
**Status:** Working Architecture
**Date:** December 2025
**Prerequisite:** [sync_resolution_problem.md](sync_resolution_problem.md)

---

## 1. Executive Summary

This document defines the complete offline sync architecture for dartwing_company DocTypes. It extends the existing `dartwing_core` sync protocol with Company-specific conflict resolution rules.

### Solution Approach

1. **Extend, Don't Replace:** Use the existing core sync infrastructure
2. **Per-DocType Rules:** Define explicit conflict strategies for each Company DocType
3. **Field-Level Granularity:** Where needed, specify per-field winner rules
4. **Custom Handlers:** Implement special merge logic for complex types (child tables, attachments)
5. **Deterministic Behavior:** No undefined states - every scenario has a defined outcome

---

## 2. Integration with Core Protocol

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUTTER CLIENT                                │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Local SQLite │  │ Sync Queue   │  │ Conflict UI  │          │
│  │ (offline DB) │  │ (pending ops)│  │ (manual res) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                    REST + Socket.IO
                          │
┌─────────────────────────┴───────────────────────────────────────┐
│                    DARTWING SYNC LAYER                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 dartwing_core.sync                        │   │
│  │  • feed()        - Change feed endpoint                   │   │
│  │  • upsert_batch()- Write queue endpoint                   │   │
│  │  • get_conflict_strategy() - Strategy lookup              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          │                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              dartwing_company.sync                        │   │
│  │  • COMPANY_CONFLICT_STRATEGIES - Company DocType rules    │   │
│  │  • merge_conversation() - Custom message merge            │   │
│  │  • validate_form_signature() - Signature handling         │   │
│  │  • resolve_appointment_conflict() - Time slot logic       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Registration

Company conflict strategies are registered with the core sync module at app initialization:

```python
# dartwing_company/hooks.py

from dartwing_core.sync.conflict_strategies import register_strategies
from dartwing_company.sync.conflict_rules import COMPANY_CONFLICT_STRATEGIES

def after_install():
    register_strategies(COMPANY_CONFLICT_STRATEGIES)
```

---

## 3. Per-DocType Conflict Strategies

### Strategy Reference

| Strategy         | Behavior                                 |
| ---------------- | ---------------------------------------- |
| `server_wins`    | Server version always takes precedence   |
| `client_wins`    | Client version takes precedence          |
| `field_level`    | Per-field winner based on configuration  |
| `manual_resolve` | Always show conflict UI to user          |
| `append_only`    | Items can only be added, never modified  |
| `version_all`    | Create version branches, never lose data |

### Complete Strategy Table

| DocType               | Strategy         | Server Wins                                   | Client Wins                                            | Notes                                       |
| --------------------- | ---------------- | --------------------------------------------- | ------------------------------------------------------ | ------------------------------------------- |
| **Dispatch Job**      | `field_level`    | status, assigned_to, scheduled_time, priority | completion_notes, photos, signature, customer_feedback | Assignment state is authoritative           |
| **Appointment**       | `manual_resolve` | -                                             | -                                                      | Time conflicts require human decision       |
| **Conversation**      | `append_only`    | -                                             | -                                                      | Messages merged as union                    |
| **Inbound Message**   | `append_only`    | -                                             | -                                                      | Never lose messages                         |
| **Ticket**            | `field_level`    | status, assigned_to, priority, sla_status     | resolution_notes, attachments, internal_notes          | Status flow is server-controlled            |
| **Vault Document**    | `version_all`    | -                                             | -                                                      | Create version on conflict                  |
| **Form Submission**   | `field_level`    | template_version, submitted_at                | field_values (except signature)                        | Signature requires manual                   |
| **Form Template**     | `server_wins`    | all                                           | -                                                      | Templates are authoritative                 |
| **Clock In Record**   | `server_wins`    | all                                           | - (exception: notes)                                   | GPS validation is authoritative             |
| **Schedule Entry**    | `server_wins`    | all                                           | -                                                      | Schedule is server-managed                  |
| **Shift Template**    | `server_wins`    | all                                           | -                                                      | Templates are authoritative                 |
| **Workflow Instance** | `server_wins`    | all                                           | -                                                      | State machine integrity                     |
| **Broadcast Alert**   | `field_level`    | status, sent_at, delivery_stats               | acknowledgment_status, acknowledged_at                 | Delivery server-tracked; ack client-reported|
| **Growth Campaign**   | `server_wins`    | all                                           | -                                                      | Campaign state is centralized               |
| **AI Call**           | `append_only`    | -                                             | -                                                      | Transcript segments appended                |
| **SLA Policy**        | `server_wins`    | all                                           | -                                                      | Policies are admin-only                     |
| **Geofence**          | `server_wins`    | all                                           | -                                                      | Boundaries are admin-only                   |

---

## 4. Implementation Details

### 4.1 Conflict Strategies Configuration

```python
# dartwing_company/sync/conflict_rules.py

COMPANY_CONFLICT_STRATEGIES = {
    # ===== OPERATIONS =====

    "Dispatch Job": {
        "strategy": "field_level",
        "server_wins_fields": [
            "status",
            "assigned_to",
            "scheduled_date",
            "scheduled_time",
            "priority",
            "estimated_duration",
            "customer",
            "address",
            "service_type",
        ],
        "client_wins_fields": [
            "completion_notes",
            "photos",
            "signature",
            "customer_feedback",
            "actual_start_time",
            "actual_end_time",
            "parts_used",
        ],
        "conflict_notification": True,
        "reason": "Assignment and scheduling are server-authoritative; field notes are tech-authoritative",
    },

    "Appointment": {
        "strategy": "manual_resolve",
        "auto_merge_fields": ["notes", "internal_notes"],
        "conflict_fields": ["appointment_date", "appointment_time", "duration"],
        "resolution_hint": "Check calendar for conflicts before resolving",
        "reason": "Time slot conflicts cannot be automatically resolved",
    },

    "Form Submission": {
        "strategy": "field_level",
        "server_wins_fields": [
            "template_version",
            "submitted_at",
            "submitted_by",
            "validation_status",
        ],
        "client_wins_fields": [
            "field_values",
            "photos",
            "notes",
        ],
        "manual_resolve_fields": ["signature"],
        "reason": "Field data from device is authoritative; signature needs human verification",
    },

    # ===== CRM =====

    "Conversation": {
        "strategy": "append_only",
        "merge_behavior": "union_of_messages",
        "child_table": "messages",
        "order_by": "timestamp",
        "dedup_key": "message_id",
        "reason": "Messages are immutable; concurrent sends should merge",
    },

    "Inbound Message": {
        "strategy": "append_only",
        "reason": "Never lose incoming messages",
    },

    "Ticket": {
        "strategy": "field_level",
        "server_wins_fields": [
            "status",
            "assigned_to",
            "priority",
            "sla_status",
            "first_response_time",
            "resolution_time",
        ],
        "client_wins_fields": [
            "resolution_notes",
            "attachments",
            "internal_notes",
        ],
        "last_write_wins_fields": ["description"],
        "reason": "Status flow and SLA are server-managed; notes are user-specific",
    },

    "Vault Document": {
        "strategy": "version_all",
        "conflict_creates_branch": True,
        "version_field": "version",
        "branch_naming": "{name}_conflict_{timestamp}",
        "reason": "Never lose document versions; conflicts create branches",
    },

    # ===== HR =====

    "Clock In Record": {
        "strategy": "server_wins",
        "exception_fields": ["notes"],
        "reason": "GPS validation is server-authoritative; time integrity is critical",
    },

    "Schedule Entry": {
        "strategy": "server_wins",
        "reason": "Schedule is centrally managed to prevent conflicts",
    },

    "Shift Template": {
        "strategy": "server_wins",
        "reason": "Templates are admin-controlled",
    },

    # ===== WORKFLOW =====

    "Workflow Instance": {
        "strategy": "server_wins",
        "reason": "State machine must be consistent; server is source of truth",
    },

    # ===== COMMUNICATIONS =====

    "Broadcast Alert": {
        "strategy": "field_level",
        "server_wins_fields": ["status", "sent_at", "delivery_stats"],
        "client_wins_fields": ["acknowledgment_status", "acknowledged_at"],
        "reason": "Delivery is server-tracked; acknowledgment is client-reported",
    },

    # ===== AI/GROWTH =====

    "Growth Campaign": {
        "strategy": "server_wins",
        "reason": "Campaign state is centrally orchestrated",
    },

    "AI Call": {
        "strategy": "append_only",
        "child_table": "transcript_segments",
        "order_by": "timestamp",
        "reason": "Transcript is append-only; segments from different sources merge",
    },

    # ===== CONFIGURATION =====

    "SLA Policy": {
        "strategy": "server_wins",
        "reason": "Policies are admin-only configuration",
    },

    "Geofence": {
        "strategy": "server_wins",
        "reason": "Geofence boundaries are admin-controlled",
    },

    "Form Template": {
        "strategy": "server_wins",
        "reason": "Templates are versioned and admin-controlled",
    },
}

# Sync configuration parameters
SYNC_CONFIG = {
    "tombstone_ttl_days": 30,
    "max_offline_duration_hours": 168,      # 7 days
    "force_reauth_after_hours": 336,        # 14 days
    "attachment_sync_priority": "metadata_first",
    "batch_upsert_size": 100,
    "conflict_notification_channel": "push",
    "manual_resolve_timeout_hours": 24,     # Auto-resolve after 24h if unresolved
    "auto_resolve_fallback": "server_wins", # Default when timeout
}
```

### 4.2 Custom Merge Handlers

For complex scenarios, custom handlers implement special logic:

```python
# dartwing_company/sync/handlers.py

from frappe import _
from dartwing_core.sync.base import ConflictHandler


class ConversationMergeHandler(ConflictHandler):
    """
    Handles conversation merges with message deduplication.
    """

    def merge(self, server_doc: dict, client_doc: dict) -> dict:
        """
        Merge conversations by unioning messages.
        Messages are deduplicated by message_id.
        Final order is by timestamp.
        """
        server_messages = server_doc.get("messages", [])
        client_messages = client_doc.get("messages", [])

        # Deduplicate by message_id
        message_map = {}
        for msg in server_messages + client_messages:
            msg_id = msg.get("message_id")
            if msg_id not in message_map:
                message_map[msg_id] = msg
            else:
                # Keep the one with earlier timestamp (first write wins for messages)
                existing = message_map[msg_id]
                if msg.get("timestamp") < existing.get("timestamp"):
                    message_map[msg_id] = msg

        # Sort by timestamp
        merged_messages = sorted(
            message_map.values(),
            key=lambda m: m.get("timestamp", "")
        )

        # Use server doc as base, replace messages
        result = server_doc.copy()
        result["messages"] = merged_messages
        result["message_count"] = len(merged_messages)

        return result


class AppointmentConflictHandler(ConflictHandler):
    """
    Detects time slot conflicts and prepares for manual resolution.
    """

    def detect_conflict(self, server_doc: dict, client_doc: dict) -> dict:
        """
        Check if appointments overlap in time.
        """
        server_start = server_doc.get("appointment_datetime")
        server_end = server_doc.get("appointment_end_datetime")
        client_start = client_doc.get("appointment_datetime")
        client_end = client_doc.get("appointment_end_datetime")

        # Check for overlap
        has_time_conflict = (
            server_start < client_end and
            client_start < server_end
        )

        return {
            "has_conflict": True,
            "conflict_type": "time_overlap" if has_time_conflict else "data_divergence",
            "server_doc": server_doc,
            "client_doc": client_doc,
            "resolution_required": True,
            "auto_mergeable_fields": ["notes", "internal_notes"],
            "conflict_fields": ["appointment_datetime", "duration"] if has_time_conflict else [],
        }


class FormSubmissionHandler(ConflictHandler):
    """
    Handles form submissions with signature validation.
    """

    def merge(self, server_doc: dict, client_doc: dict) -> dict:
        """
        Merge form fields, flag signature for manual review.
        """
        result = server_doc.copy()

        # Client wins for field values (they have the actual data)
        if client_doc.get("field_values"):
            result["field_values"] = client_doc["field_values"]

        # Client wins for photos
        if client_doc.get("photos"):
            result["photos"] = client_doc["photos"]

        # Signature requires special handling
        server_sig = server_doc.get("signature")
        client_sig = client_doc.get("signature")

        if server_sig != client_sig:
            # Both have different signatures - flag for manual review
            result["_signature_conflict"] = True
            result["_server_signature"] = server_sig
            result["_client_signature"] = client_sig
            result["signature"] = client_sig  # Default to client, but flag it
            result["validation_status"] = "pending_signature_review"

        return result


# Register handlers
CUSTOM_HANDLERS = {
    "Conversation": ConversationMergeHandler,
    "Appointment": AppointmentConflictHandler,
    "Form Submission": FormSubmissionHandler,
}
```

### 4.3 Attachment Sync Strategy

```python
# dartwing_company/sync/attachments.py

ATTACHMENT_SYNC_CONFIG = {
    # Sync metadata first, lazy-load actual files
    "strategy": "metadata_first",

    # Maximum file size to auto-sync (larger files require explicit download)
    "auto_sync_max_bytes": 5 * 1024 * 1024,  # 5MB

    # File types that always sync (critical for operations)
    "always_sync_types": [
        "image/jpeg",
        "image/png",
        "application/pdf",  # Signatures, forms
    ],

    # File types to defer (large, less critical)
    "defer_sync_types": [
        "video/*",
        "application/zip",
    ],

    # Thumbnail generation for images
    "generate_thumbnails": True,
    "thumbnail_max_dimension": 200,

    # Conflict handling for attachments
    "attachment_conflict": "keep_both",  # Never lose attachments

    # Cleanup policy
    "local_cache_max_mb": 500,
    "local_cache_eviction": "lru",  # Least recently used
}
```

### 4.4 Mobile Client Responsibilities

The Flutter client must implement these behaviors:

```dart
// lib/sync/sync_manager.dart (conceptual)

class SyncManager {
  /// Queue local changes with timestamp
  Future<void> queueChange(String doctype, String name, Map<String, dynamic> data) async {
    await localQueue.add(QueuedChange(
      doctype: doctype,
      name: name,
      data: data,
      clientTimestamp: DateTime.now().toIso8601String(),
      operation: data['name'] == null ? 'insert' : 'update',
    ));
  }

  /// Process sync response, handle conflicts
  Future<void> processSyncResponse(SyncResponse response) async {
    for (final item in response.items) {
      if (item.status == 'conflict') {
        await handleConflict(item);
      } else if (item.status == 'success') {
        await applyServerUpdate(item.resolvedDoc);
      }
    }
  }

  /// Handle conflict based on strategy
  Future<void> handleConflict(ConflictItem item) async {
    final strategy = item.conflictStrategy;

    switch (strategy) {
      case 'server_wins':
        // Accept server version, notify user
        await applyServerUpdate(item.serverDoc);
        await showNotification('Your changes were overwritten by server');
        break;

      case 'client_wins':
        // Resubmit with force flag
        await resubmitWithForce(item.clientDoc);
        break;

      case 'field_level':
        // Merge fields according to rules
        final merged = mergeFields(item.serverDoc, item.clientDoc, item.fieldRules);
        await submitMerged(merged);
        break;

      case 'manual_resolve':
        // Show conflict resolution UI
        await showConflictResolutionUI(item);
        break;

      case 'append_only':
        // Merge as union (already handled by server)
        await applyServerUpdate(item.resolvedDoc);
        break;

      case 'version_all':
        // Server created a branch, notify user
        await applyServerUpdate(item.resolvedDoc);
        await showNotification('A version branch was created due to conflict');
        break;
    }
  }
}
```

---

## 5. Edge Cases & Special Handling

### 5.1 Child Table Merging

For DocTypes with child tables (messages, line items), special merge logic applies:

```python
# Child table merge rules

CHILD_TABLE_MERGE_RULES = {
    "Conversation": {
        "child_field": "messages",
        "merge_strategy": "union",
        "dedup_key": "message_id",
        "order_by": "timestamp",
        "conflict_on_same_key": "first_write_wins",
    },

    "Dispatch Job": {
        "child_field": "parts_used",
        "merge_strategy": "union",
        "dedup_key": "item_code",
        "conflict_on_same_key": "sum_quantities",  # Add quantities together
    },

    "AI Call": {
        "child_field": "transcript_segments",
        "merge_strategy": "union",
        "dedup_key": "segment_id",
        "order_by": "start_time",
    },
}
```

### 5.2 Linked Document Changes

When a linked document changes (e.g., Customer address), cached data in Company DocTypes may become stale:

```python
# dartwing_company/events/linked_doc_sync.py

def on_address_update(doc, method):
    """
    When an ERPNext Address is updated, flag related Dispatch Jobs
    for sync refresh.
    """
    # Find all Dispatch Jobs linking to this address
    jobs = frappe.get_all(
        "Dispatch Job",
        filters={
            "address": doc.name,
            "status": ["not in", ["Completed", "Cancelled"]],
        },
        pluck="name"
    )

    for job_name in jobs:
        # Mark for sync refresh (clients will re-fetch)
        frappe.publish_realtime(
            "sync_refresh",
            {"doctype": "Dispatch Job", "name": job_name},
            room=f"sync:Dispatch Job:{get_org_for_job(job_name)}"
        )


def on_customer_update(doc, method):
    """
    When an ERPNext Customer is updated, notify related records.
    """
    # Similar pattern for Appointments, Tickets, etc.
    pass
```

### 5.3 Tombstone Handling

Deleted records must be tracked to prevent resurrection:

```python
# Tombstone rules per DocType

TOMBSTONE_RULES = {
    "Dispatch Job": {
        "allow_delete": False,  # Soft delete only (status = Cancelled)
        "tombstone_ttl_days": 90,
    },

    "Conversation": {
        "allow_delete": False,  # Never delete conversations
        "archive_after_days": 365,
    },

    "Form Submission": {
        "allow_delete": False,  # Legal record
        "tombstone_ttl_days": 2555,  # 7 years
    },

    "Ticket": {
        "allow_delete": True,
        "tombstone_ttl_days": 30,
        "tombstone_wins_over_update": True,
    },

    "_default": {
        "allow_delete": True,
        "tombstone_ttl_days": 30,
        "tombstone_wins_over_update": True,
    },
}
```

---

## 6. Testing Requirements

### 6.1 Unit Tests

```python
# tests/sync/test_conflict_strategies.py

class TestDispatchJobConflict:
    def test_server_wins_for_assignment(self):
        """Server assignment takes precedence over client."""
        server = {"assigned_to": "TECH-002", "status": "In Progress"}
        client = {"assigned_to": "TECH-001", "status": "Assigned"}

        result = resolve_conflict("Dispatch Job", server, client)

        assert result["assigned_to"] == "TECH-002"  # Server wins
        assert result["status"] == "In Progress"    # Server wins

    def test_client_wins_for_notes(self):
        """Client completion notes take precedence."""
        server = {"completion_notes": ""}
        client = {"completion_notes": "Fixed the issue"}

        result = resolve_conflict("Dispatch Job", server, client)

        assert result["completion_notes"] == "Fixed the issue"  # Client wins


class TestConversationMerge:
    def test_messages_union(self):
        """Messages from both sources are merged."""
        server = {"messages": [{"message_id": "A", "text": "Hello"}]}
        client = {"messages": [{"message_id": "B", "text": "Hi"}]}

        result = resolve_conflict("Conversation", server, client)

        assert len(result["messages"]) == 2
        assert {"message_id": "A", "text": "Hello"} in result["messages"]
        assert {"message_id": "B", "text": "Hi"} in result["messages"]

    def test_message_deduplication(self):
        """Duplicate messages are deduplicated."""
        server = {"messages": [{"message_id": "A", "text": "Hello"}]}
        client = {"messages": [{"message_id": "A", "text": "Hello"}]}

        result = resolve_conflict("Conversation", server, client)

        assert len(result["messages"]) == 1
```

### 6.2 Integration Tests

```python
# tests/sync/test_offline_scenarios.py

class TestOfflineScenarios:
    def test_tech_offline_job_reassigned(self):
        """
        Scenario: Tech goes offline, job is reassigned, tech syncs.
        Expected: Tech sees new assignment, their local changes preserved.
        """
        # Setup
        job = create_dispatch_job(assigned_to="TECH-A")
        simulate_tech_offline("TECH-A")

        # Tech A adds completion notes while offline
        tech_a_changes = {"completion_notes": "Started work"}
        queue_offline_change("TECH-A", job.name, tech_a_changes)

        # Office reassigns to Tech B
        job.assigned_to = "TECH-B"
        job.save()

        # Tech A comes online
        sync_result = sync_client("TECH-A")

        # Assertions
        assert job.reload().assigned_to == "TECH-B"  # Server wins
        assert "completion_notes" in sync_result.conflicts  # Note flagged
        assert sync_result.notifications[0].type == "assignment_changed"

    def test_appointment_double_booking(self):
        """
        Scenario: Two receptionists book same slot offline.
        Expected: Manual resolution required.
        """
        # Both create appointments for 2pm
        apt_a = create_appointment_offline("RECEPT-A", time="14:00")
        apt_b = create_appointment_offline("RECEPT-B", time="14:00")

        # Sync both
        result_a = sync_client("RECEPT-A")
        result_b = sync_client("RECEPT-B")

        # One should succeed, one should require manual resolution
        assert (
            result_a.status == "success" and result_b.status == "conflict_manual"
        ) or (
            result_b.status == "success" and result_a.status == "conflict_manual"
        )
```

### 6.3 Test Matrix

| Scenario                        | DocType         | Strategy       | Expected Behavior       |
| ------------------------------- | --------------- | -------------- | ----------------------- |
| Assignment change while offline | Dispatch Job    | field_level    | Server wins assignment  |
| Notes added while offline       | Dispatch Job    | field_level    | Client wins notes       |
| Time slot conflict              | Appointment     | manual_resolve | UI shown to user        |
| Message sent offline            | Conversation    | append_only    | Messages merged         |
| Status changed by two users     | Ticket          | field_level    | Server wins status      |
| Form filled offline             | Form Submission | field_level    | Client wins fields      |
| Signature conflict              | Form Submission | manual_resolve | Flag for review         |
| Clock-in GPS dispute            | Clock In Record | server_wins    | Server is authoritative |
| Document edited offline         | Vault Document  | version_all    | Branch created          |

---

## 7. Rollout Plan

### Phase 1: Foundation (Week 1-2)

1. **Implement COMPANY_CONFLICT_STRATEGIES dict**

   - File: `dartwing_company/sync/conflict_rules.py`
   - All 16 DocTypes defined

2. **Register with core sync module**

   - Hook in `after_install`
   - Verify strategies load correctly

3. **Unit tests for all strategies**
   - 100% coverage of strategy logic

### Phase 2: Custom Handlers (Week 3-4)

1. **Implement ConversationMergeHandler**

   - Message deduplication
   - Timestamp ordering

2. **Implement AppointmentConflictHandler**

   - Time overlap detection
   - Manual resolve UI data

3. **Implement FormSubmissionHandler**
   - Signature conflict flagging

### Phase 3: Flutter Client (Week 5-6)

1. **Update sync_manager.dart**

   - Handle all strategy types
   - Conflict resolution UI

2. **Conflict Resolution UI**
   - Side-by-side diff view
   - Field-level picker
   - Manual edit option

### Phase 4: Integration Testing (Week 7-8)

1. **Run full test matrix**

   - All scenarios from Section 6.3

2. **Load testing**

   - 100 concurrent offline syncs
   - Conflict rate under 5%

3. **Edge case validation**
   - Child table merging
   - Attachment sync
   - Tombstone handling

### Phase 5: Staged Rollout (Week 9-10)

1. **Internal testing (Week 9)**

   - All team members use offline mode
   - Log conflicts, verify resolution

2. **Beta customers (Week 10)**

   - 5 customers with heavy mobile usage
   - Monitor conflict rates

3. **General availability**
   - Enable for all customers
   - Monitor metrics

---

## 8. Success Metrics

| Metric                 | Target            | Measurement                   |
| ---------------------- | ----------------- | ----------------------------- |
| Conflict rate          | < 2% of syncs     | `conflicts / total_syncs`     |
| Manual resolution rate | < 5% of conflicts | `manual_resolves / conflicts` |
| Data loss incidents    | 0                 | Support tickets + logs        |
| Sync latency p99       | < 5s              | Backend metrics               |
| Client satisfaction    | > 4.5/5           | In-app survey after conflict  |

---

## 9. References

- [dartwing_core/offline_real_time_sync_spec.md](../../dartwing_core/offline_real_time_sync_spec.md) - Core sync protocol
- [sync_resolution_problem.md](sync_resolution_problem.md) - Problem statement
- [review_company_arch.md](review_company_arch.md) - Architecture gap analysis

---

_Document created: December 2025_
_Status: Working Architecture - Ready for Implementation_
