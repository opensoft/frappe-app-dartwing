# Dartwing Company Architecture Review Plan

**Date:** December 2025
**Purpose:** Consolidated analysis of architecture critiques and action plan for outstanding gaps
**Architecture Maturity:** 94%

---

## 1. Executive Summary

Three independent reviewers (Gemi, Jeni, Claude) have analyzed the Dartwing Company architecture. The architecture has matured significantly with the addition of Sections 10-16, addressing most critical concerns. However, **9 gaps remain** that require specification before the platform is production-ready.

### Current Status

| Category               | Status | Notes                                        |
| ---------------------- | ------ | -------------------------------------------- |
| Integration Patterns   | 95%    | Excellent ERPNext/HRMS/CRM integration       |
| DocType Schemas        | 98%    | Section 15 added full JSON schemas           |
| Error Handling         | 95%    | Section 10 added retry/circuit breaker       |
| Transaction Management | 95%    | Section 11 added Saga patterns               |
| Caching                | 95%    | Section 12 added multi-layer strategy        |
| Offline Sync           | 85%    | Protocol adopted, **conflict rules missing** |
| Observability          | 50%    | **Critical gap**                             |
| Multi-Tenancy          | 80%    | Permission inheritance **undefined**         |
| Dispatch Performance   | 98%    | SQL-optimized in Section 5.2                 |

---

## 2. Reviewer Consensus

All three reviewers agreed on these key points:

### Strengths

1. **Overlay Strategy** - "Don't extend, overlay" is the right approach for Frappe ecosystem
2. **Event-Driven** - Using `doc_events` for loose coupling is sound
3. **SQL-Optimized Dispatch** - Section 5.2 resolved the O(n) scalability issue
4. **API-First** - Essential for Flutter mobile app integration

### Shared Concerns

1. **"Sync Hell" Risk** - The overlay pattern creates data consistency risks when hooks fail
2. **Offline Conflict Resolution** - No per-DocType merge strategies defined
3. **Permission Gaps** - Multi-tenant permission inheritance unclear
4. **AI Feature Risks** - Voice latency, RAG scalability, content filtering under-specified

---

## 3. Outstanding Gaps

### Gap 1: Offline Sync Conflict Resolution (CRITICAL)

**Problem:** The architecture adopts the Dartwing Core sync protocol but doesn't specify conflict resolution strategies per DocType.

**Required Specification:**

```python
# dartwing_company/sync/conflict_rules.py

COMPANY_CONFLICT_STRATEGIES = {
    # ===== OPERATIONS =====
    "Dispatch Job": {
        "strategy": "field_level",
        "server_wins_fields": ["status", "assigned_to", "scheduled_time", "priority"],
        "client_wins_fields": ["completion_notes", "photos", "signature"],
        "reason": "Central scheduler has authoritative assignment state",
    },

    "Appointment": {
        "strategy": "manual_resolve",
        "reason": "Time conflicts require customer communication",
        "auto_merge_fields": ["notes", "internal_notes"],
    },

    "Form Submission": {
        "strategy": "field_level",
        "server_wins_fields": ["template_version", "submitted_at"],
        "client_wins_fields": ["field_values", "photos"],
        "manual_resolve_fields": ["signature"],
        "reason": "Field data authoritative; signature needs verification",
    },

    # ===== CRM =====
    "Conversation": {
        "strategy": "append_only",
        "reason": "Messages are immutable once sent",
        "merge_behavior": "union_of_messages",
    },

    "Inbound Message": {
        "strategy": "append_only",
        "reason": "Never lose incoming messages",
    },

    "Ticket": {
        "strategy": "field_level",
        "server_wins_fields": ["status", "assigned_to", "priority", "sla_status"],
        "client_wins_fields": ["resolution_notes", "attachments"],
        "last_write_wins_fields": ["description"],
    },

    "Vault Document": {
        "strategy": "version_all",
        "reason": "Never lose document versions",
        "conflict_creates_branch": True,
    },

    # ===== HR =====
    "Clock In Record": {
        "strategy": "server_wins",
        "exception_fields": ["notes"],  # Notes can be updated by client
        "reason": "GPS validation must be authoritative",
    },

    "Schedule Entry": {
        "strategy": "server_wins",
        "reason": "Schedule is centrally managed",
    },

    "Shift Template": {
        "strategy": "server_wins",
        "reason": "Templates are admin-controlled",
    },

    # ===== WORKFLOW & COMMS =====
    "Workflow Instance": {
        "strategy": "server_wins",
        "reason": "State machine integrity",
    },

    "Broadcast Alert": {
        "strategy": "field_level",
        "server_wins_fields": ["status", "sent_at", "delivery_stats"],
        "client_wins_fields": ["acknowledgment_status", "acknowledged_at"],
        "reason": "Delivery is server-tracked; acknowledgment is client-reported",
    },

    # ===== AI & CONFIG =====
    "Growth Campaign": {
        "strategy": "server_wins",
        "reason": "Campaign state is centralized",
    },

    "AI Call": {
        "strategy": "append_only",
        "child_table": "transcript_segments",
    },

    "SLA Policy": {"strategy": "server_wins"},
    "Geofence": {"strategy": "server_wins"},
    "Form Template": {"strategy": "server_wins"},
}

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

ATTACHMENT_SYNC_CONFIG = {
    "strategy": "metadata_first",
    "auto_sync_max_bytes": 5242880,  # 5MB
    "always_sync_types": ["image/jpeg", "application/pdf"],
    "attachment_conflict": "keep_both",
}

TOMBSTONE_RULES = {
    "Dispatch Job": {"allow_delete": False},
    "Conversation": {"allow_delete": False},
    "Form Submission": {"allow_delete": False},
    "_default": {"allow_delete": True, "tombstone_ttl_days": 30},
}

CHILD_TABLE_MERGE_RULES = {
    "Conversation": {
        "child_field": "messages",
        "merge_strategy": "union",
        "dedup_key": "message_id",
    },
    "AI Call": {
        "child_field": "transcript_segments",
        "merge_strategy": "union",
    },
}
```

**Implementation Priority:** Pre-Wave A

---

### Gap 2: Observability Metrics (HIGH)

**Problem:** No defined metrics for dispatch, messaging, sync, AI, or SLA tracking.

**Required Specification:**

```python
# dartwing_company/observability/metrics.py

CRITICAL_METRICS = {
    "dispatch": {
        "assignment_latency_p99": {
            "query": "histogram_quantile(0.99, dispatch_assignment_duration_seconds)",
            "threshold": "< 5s",
            "alert_if_exceeded_for": "5m",
        },
        "unassigned_jobs_count": {
            "query": "count(dispatch_job_status{status='unassigned'})",
            "threshold": "> 10",
            "alert_if_exceeded_for": "5m",
        },
        "job_completion_rate": {
            "query": "rate(dispatch_job_completed_total[1h]) / rate(dispatch_job_created_total[1h])",
            "threshold": "> 0.95",
        },
    },

    "messaging": {
        "delivery_latency_p95_by_channel": {
            "query": "histogram_quantile(0.95, message_delivery_duration_seconds) by (channel)",
            "thresholds": {"email": "< 30s", "sms": "< 10s", "whatsapp": "< 5s"},
        },
        "dlq_depth": {
            "query": "sum(dead_letter_queue_depth) by (channel)",
            "threshold": "> 50",
            "alert_if_exceeded_for": "10m",
        },
    },

    "sync": {
        "sync_lag_seconds": {
            "query": "max(time() - last_sync_timestamp) by (device_id)",
            "threshold": "> 300",
        },
        "conflict_manual_rate": {
            "query": "rate(sync_conflict_manual_total[1d]) / rate(sync_conflict_total[1d])",
            "threshold": "< 0.05",
        },
        "sync_failure_rate": {
            "query": "rate(sync_failed_total[1h]) / rate(sync_attempted_total[1h])",
            "threshold": "< 0.01",
        },
    },

    "ai": {
        "response_latency_p99": {
            "query": "histogram_quantile(0.99, ai_request_duration_seconds)",
            "threshold": "< 3s",
        },
        "fallback_rate": {
            "query": "rate(ai_fallback_triggered_total[1h]) / rate(ai_request_total[1h])",
            "threshold": "< 0.1",
        },
        "cost_per_org_daily": {
            "query": "sum(ai_token_cost_dollars) by (organization)",
            "alert_if": "> $50 per org per day",
        },
    },

    "sla": {
        "breach_rate": {
            "query": "rate(ticket_sla_breached_total[1d]) / rate(ticket_created_total[1d])",
            "threshold": "< 0.05",
        },
        "first_response_time_p90": {
            "query": "histogram_quantile(0.90, ticket_first_response_seconds)",
            "threshold": "< 3600",
        },
    },
}

ALERT_CHANNELS = {
    "critical": ["pagerduty", "slack:#incidents"],
    "warning": ["slack:#ops-alerts"],
    "info": ["slack:#ops-metrics"],
}
```

**Implementation Priority:** Pre-Wave A

---

### Gap 3: Multi-Tenancy Permission Inheritance (HIGH)

**Problem:** `parent_org` support mentioned but permission inheritance rules undefined.

**Required Specification:**

```python
# dartwing_company/permissions/hierarchy.py

from enum import Enum

class HierarchyMode(Enum):
    STRICT_ISOLATION = "strict"      # No visibility between parent/child
    PARENT_OVERSIGHT = "oversight"   # Parent sees child data (read-only)
    SHARED_RESOURCES = "shared"      # Specific DocTypes shared

# Default configuration (recommended for v1)
DEFAULT_HIERARCHY = {
    "mode": "STRICT_ISOLATION",
}

# Franchise model
FRANCHISE_HIERARCHY = {
    "mode": "PARENT_OVERSIGHT",
    "parent_can_see": ["Ticket", "Dispatch Job", "Employee"],
    "parent_can_edit": [],  # Read-only
    "billing_aggregation": "aggregate_to_parent",
}

# Holding company
HOLDING_HIERARCHY = {
    "mode": "SHARED_RESOURCES",
    "shared_doctypes": ["Employee", "Vault Document", "Knowledge Base"],
    "isolated_doctypes": ["Conversation", "Ticket", "Dispatch Job"],
}

def get_permission_query_for_hierarchy(user, doctype, hierarchy_config):
    """Build permission query considering org hierarchy."""
    user_orgs = get_user_organizations(user)

    if hierarchy_config["mode"] == "STRICT_ISOLATION":
        return f"`organization` IN ({format_list(user_orgs)})"

    elif hierarchy_config["mode"] == "PARENT_OVERSIGHT":
        visible_orgs = set(user_orgs)
        for org in user_orgs:
            if is_parent_org(org):
                visible_orgs.update(get_child_orgs(org))

        if doctype in hierarchy_config.get("parent_can_see", []):
            return f"`organization` IN ({format_list(visible_orgs)})"
        return f"`organization` IN ({format_list(user_orgs)})"

    elif hierarchy_config["mode"] == "SHARED_RESOURCES":
        if doctype in hierarchy_config.get("shared_doctypes", []):
            hierarchy_orgs = get_full_hierarchy_orgs(user_orgs)
            return f"`organization` IN ({format_list(hierarchy_orgs)})"
        return f"`organization` IN ({format_list(user_orgs)})"
```

**Implementation Priority:** Pre-Wave A

---

### Gap 4: Background Job Queue Isolation (HIGH)

**Problem:** No strategy for isolating background jobs to prevent "noisy neighbor" issues.

**Required Specification:**

```python
# dartwing_company/jobs/queue_strategy.py

QUEUE_STRATEGY = {
    "default": {
        "type": "shared",
        "workers": 4,
        "priority": "normal",
    },

    "critical": {
        "type": "per_org",
        "workers": 2,
        "priority": "high",
        "doctypes": ["Dispatch Job", "Broadcast Alert"],
        "reason": "Prevent noisy neighbor; SLA-bound operations",
    },

    "bulk": {
        "type": "rate_limited",
        "workers": 1,
        "max_per_minute": 100,
        "doctypes": ["Broadcast Alert", "Import Job"],
        "reason": "Prevent resource exhaustion",
    },

    "ai": {
        "type": "dedicated",
        "workers": 2,
        "timeout_seconds": 30,
        "doctypes": ["AI Call", "Growth Campaign", "Ask Anything Query"],
        "reason": "Predictable latency; prevent blocking other jobs",
    },
}
```

**Implementation Priority:** Pre-Wave B

---

### Gap 5: DR/RTO/RPO Specification (HIGH)

**Problem:** No disaster recovery objectives defined.

**Required Specification:**

```yaml
# dartwing_company/deployment/disaster_recovery.yaml

recovery_objectives:
  rpo: # Recovery Point Objective (max data loss)
    dispatch_jobs: 5 minutes # Active jobs are critical
    conversations: 1 hour
    vault_documents: 15 minutes
    appointments: 1 hour
    tickets: 1 hour
    ai_calls: 24 hours # Can regenerate from logs

  rto: # Recovery Time Objective (max downtime)
    core_api: 15 minutes
    portal: 30 minutes
    search: 1 hour
    ai_features: 4 hours # Degrade gracefully
    reporting: 8 hours

backup_strategy:
  database:
    frequency: continuous # WAL streaming
    retention: 30 days
    geo_redundancy: true
    test_restore_frequency: weekly

  files:
    frequency: hourly
    retention: 90 days
    storage: S3 cross-region replication

  redis:
    frequency: 15 minutes
    retention: 7 days
    note: "Ephemeral - can rebuild from DB"

failover_procedures:
  database_failure:
    automatic: true
    detection_time: 30 seconds
    failover_time: 60 seconds

  api_server_failure:
    automatic: true
    health_check_interval: 10 seconds
    unhealthy_threshold: 3
    replacement_time: 120 seconds

  ai_service_failure:
    automatic: true
    fallback: "queue_for_retry"
    max_retry_hours: 4
    user_notification: "AI features temporarily unavailable"
```

**Implementation Priority:** Pre-Wave C

---

### Gap 6: Wave Readiness Gates (MEDIUM)

**Problem:** Waves defined but lack explicit readiness criteria.

**Required Specification:**

```yaml
# dartwing_company/deployment/wave_gates.yaml

waves:
  wave_a:
    name: "Portal + Vault + Appointments + Basic Tickets"
    doctypes: [Customer Portal, Vault Document, Appointment, Ticket]
    readiness_gates:
      technical:
        - name: core_multi_tenant_working
          test: "pytest tests/multi_tenancy/ -v"
          required: true
        - name: permission_isolation_verified
          test: "pytest tests/permissions/cross_org_isolation.py"
          required: true
      operational:
        - name: staging_load_test_passed
          metric: "p99_latency < 500ms at 100 concurrent users"
          required: true
        - name: security_scan_passed
          tool: "OWASP ZAP baseline scan"
          required: true

  wave_b:
    name: "Inbox + Workflow + Broadcast"
    doctypes:
      [Conversation, Inbound Message, Workflow Template, Broadcast Alert]
    readiness_gates:
      technical:
        - name: wave_a_in_production
          check: "wave_a.status == 'deployed' AND wave_a.uptime_7d > 99.5%"
          required: true
        - name: rate_limiting_implemented
          test: "pytest tests/rate_limits/"
          required: true
      operational:
        - name: dlq_monitoring_active
          check: "dead_letter_queue.alerts_configured == true"
          required: true

  wave_c:
    name: "Dispatch + Geo Clock-In"
    doctypes: [Dispatch Job, Clock In Record, Geofence]
    readiness_gates:
      technical:
        - name: wave_b_in_production
          required: true
        - name: offline_sync_stable
          test: "pytest tests/sync/offline_scenarios.py"
          required: true
      operational:
        - name: maps_api_quota_verified
          check: "google_maps.monthly_quota > estimated_usage * 1.5"
          required: true

  wave_d:
    name: "AI Receptionist + Growth + Ask Anything"
    doctypes: [AI Call, Growth Campaign, Search Query]
    readiness_gates:
      technical:
        - name: wave_c_in_production
          required: true
        - name: content_filtering_audited
          audit: "manual review of AI output filtering"
          required: true
      operational:
        - name: ai_cost_monitoring_active
          check: "openai.spend_alerts_configured == true"
          required: true
```

**Implementation Priority:** Pre-Wave A

---

### Gap 7: API Versioning Strategy (MEDIUM)

**Problem:** No API versioning policy defined.

**Required Specification:**

```python
# dartwing_company/api/versioning.py

API_VERSIONS = {
    "v1": {
        "status": "stable",
        "deprecation_date": None,
        "endpoints": "/api/v1/company/*",
    },
    "v2": {
        "status": "current",
        "breaking_changes": ["ticket_schema", "dispatch_response"],
        "endpoints": "/api/v2/company/*",
    },
    "beta": {
        "status": "experimental",
        "stability": "no guarantees",
        "endpoints": "/api/beta/company/ai_*",
        "requires_flag": "enable_beta_api",
    },
}

def get_api_version(request):
    # Check header first
    version = request.headers.get("X-API-Version")
    if version:
        return version

    # Check URL path
    if "/v2/" in request.path:
        return "v2"
    if "/beta/" in request.path:
        return "beta"

    return "v1"  # Default
```

**Implementation Priority:** Pre-Wave B

---

### Gap 8: Feature Flags per Organization (MEDIUM)

**Problem:** No per-org feature enablement infrastructure.

**Required Specification:**

```python
# dartwing_company/doctype/org_feature_flags/org_feature_flags.py

class OrgFeatureFlags(Document):
    """Per-organization feature flag configuration."""

    # Wave gating
    enable_dispatch: DF.Check = False
    enable_ai_receptionist: DF.Check = False
    enable_growth_orchestrator: DF.Check = False
    enable_universal_inbox: DF.Check = False

    # Compliance modes
    hipaa_mode: DF.Check = False
    gdpr_mode: DF.Check = False
    sox_audit_mode: DF.Check = False

    # Limits
    max_broadcast_per_day: DF.Int = 1000
    max_ai_requests_per_hour: DF.Int = 100
    max_dispatch_jobs_per_day: DF.Int = 500

    # Beta features
    enable_beta_api: DF.Check = False
    enable_experimental_ai: DF.Check = False


def is_feature_enabled(organization: str, feature: str) -> bool:
    """Check if feature is enabled for organization."""
    flags = frappe.get_cached_doc("Org Feature Flags", {"organization": organization})
    return getattr(flags, feature, False)
```

**Implementation Priority:** Pre-Wave A

---

### Gap 9: HIPAA Compliance (MEDIUM - if health mode enabled)

**Problem:** Healthcare overlay lacks HIPAA-specific controls.

**Required Specification:**

```python
# dartwing_company/compliance/hipaa.py

PHI_DOCTYPES = [
    "Patient Record",
    "Medical Note",
    "Appointment",      # If contains medical reason
    "Conversation",     # If patient communications
    "Vault Document",   # If contains medical docs
]

HIPAA_REQUIREMENTS = {
    "access_controls": {
        "minimum_necessary": {
            "description": "Field-level filtering based on role",
            "implementation": "Dynamic field permissions per DocType",
        },
        "break_glass": {
            "description": "Emergency access with audit + notification",
            "max_duration_hours": 4,
            "notification_recipients": ["privacy_officer", "supervisor"],
        },
        "automatic_logoff": {
            "session_timeout_minutes": 15,
            "idle_warning_minutes": 12,
        },
    },

    "audit_logging": {
        "phi_access_log": {
            "retention_years": 6,
            "fields": ["who", "what", "when", "why", "from_ip", "device_id"],
            "immutable": True,
        },
    },

    "encryption": {
        "at_rest": {"algorithm": "AES-256"},
        "in_transit": {"minimum_tls": "1.2"},
    },

    "baa_tracking": {
        "required_for": [
            "Cloud hosting provider",
            "Email service (if PHI in emails)",
            "SMS provider (if PHI in messages)",
            "AI/LLM provider (if processing PHI)",
        ],
        "tracking_fields": [
            "vendor_name", "baa_signed_date", "baa_expiry_date",
            "data_categories_shared", "last_security_review",
        ],
    },

    "retention": {
        "medical_records": {"retention_years": 7},
        "audit_logs": {"retention_years": 6, "cannot_be_modified": True},
    },
}
```

**Implementation Priority:** Pre-Wave D (if healthcare features enabled)

---

## 4. Implementation Priority by Wave

```
PRE-WAVE A (Foundation) - MUST COMPLETE FIRST:
├─ Gap 1: Conflict resolution rules per DocType (Critical)
├─ Gap 3: Permission inheritance for parent_org (High)
├─ Gap 2: Critical metrics dashboard (High)
├─ Gap 8: Feature flags infrastructure (Medium)
└─ Gap 6: Wave readiness gates definition (Medium)

PRE-WAVE B (Inbox/Workflow):
├─ Gap 4: Job queue isolation (High)
├─ Gap 7: API versioning (Medium)
└─ DLQ monitoring (from Gap 2)

PRE-WAVE C (Dispatch/HR):
├─ Gap 5: DR runbook and testing (High)
└─ Sync lag metrics (from Gap 2)

PRE-WAVE D (AI Features):
├─ Gap 9: HIPAA compliance (Medium - if health data)
├─ AI cost monitoring (from Gap 2)
└─ Break-glass access (from Gap 9)
```

---

## 5. Cross-References

### Source Critiques

- [critique_arch_company_gemi.md](critique_arch_company_gemi.md) - Sync Hell, dispatch scalability, offline ambiguity
- [critique_arch_company_jeni.md](critique_arch_company_jeni.md) - Missing schemas, permissions, offline sync
- [critique_arch_company_claude.md](critique_arch_company_claude.md) - Comprehensive 94% review with gap analysis
- [sync_resolution_problem.md](sync_resolution_problem.md) - Detailed analysis of sync risks and scenarios
- [sync_resolution_plan.md](sync_resolution_plan.md) - Complete technical specification for sync resolution

### Architecture Sections Addressing Previous Issues

- Section 5.2: SQL-Optimized SmartAssignment
- Section 10: Error Handling Patterns
- Section 11: Transaction/Saga Management
- Section 12: Caching Strategy
- Section 13: Offline Sync Protocol Adoption
- Section 14: Reconciliation Jobs
- Section 15: DocType JSON Schemas
- Section 16: Permission Framework

---

## 6. Summary

The Dartwing Company architecture is **94% production-ready**. The 9 gaps identified in this document represent the final specifications needed before confident deployment. The most critical items are:

1. **Conflict Resolution Rules** - Without these, offline sync will cause data loss
2. **Observability Metrics** - Without these, production issues will be invisible
3. **Permission Inheritance** - Without this, multi-tenant security is incomplete

Addressing all 9 gaps in the order specified will ensure the platform is robust, secure, and maintainable at scale.

---

_Document created: December 2025_
_Last revised: December 2025 - Integrated sync resolution specifications_
_Based on reviews by: Gemi, Jeni, Claude_
_Architecture version: Dartwing Company 1.0_
