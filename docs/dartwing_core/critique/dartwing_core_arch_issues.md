# Claude's Dartwing Core Architecture Critique

**Focus: Core Platform Architecture vs PRD Implementation Feasibility**

**Status: November 2025 (Updated after specification work)**

---

## Resolution Status

| Issue | Status | Resolution |
|-------|--------|------------|
| Socket.IO horizontal scaling | ✅ RESOLVED | See `socket_io_scaling_spec.md` |
| Integration token management | ✅ RESOLVED | See `integration_token_management_spec.md` |
| Per-DocType conflict rules | ✅ RESOLVED | See `offline_real_time_sync_spec.md` (updated) |
| Full-stack observability | ✅ RESOLVED | See `observability_spec.md` |
| Background job isolation | ✅ RESOLVED | See `background_job_isolation_spec.md` |
| AI infrastructure | ⏳ PENDING | Requires dedicated sprint |
| Permission query optimization | ⏳ PENDING | P2 priority |
| Compliance enforcement | ⏳ PENDING | P2 priority |

---

## Executive Summary

The Dartwing Core architecture (~1,540 lines) provides a **solid foundation** for a multi-tenant platform built on Frappe/Flutter. The PRD (~5,000 lines) defines 22+ core features with ambitious scope spanning compliance, AI, integrations, and developer experience.

**Overall Assessment:** The architecture is **85-90% production-ready** for the PRD requirements after specification work. Remaining gaps:

1. ~~**Offline sync conflict resolution**~~ ✅ RESOLVED - Per-DocType strategies now defined
2. **AI infrastructure** - High-level design without implementation details (P2)
3. ~~**Integration token management**~~ ✅ RESOLVED - Full lifecycle specified
4. ~~**Real-time scaling**~~ ✅ RESOLVED - Redis adapter pattern documented
5. ~~**Observability**~~ ✅ RESOLVED - Full-stack metrics and alerting defined

The architecture can support PRD implementation with the specifications now in place.

---

## Part 1: Architecture Strengths

### 1.1 Multi-Tenancy Model

The Organization → Concrete Type (Family/Company/Nonprofit/Club) hierarchy is **well-designed**:

```
Organization (abstract)
├── Company (concrete type)
├── Family (concrete type)
├── Nonprofit (concrete type)
└── Club (concrete type)
```

**Strengths:**

- Clean separation between org types
- Shared core features with type-specific extensions
- Permission isolation via `organization` field on all DocTypes
- Supports the PRD's multi-org switching requirement (C-03)

### 1.2 Person Model & Identity Management

The Person doctype (defined in `person_doctype_contract.md`) provides unified identity management:

```
Person (single doctype)
├── Identity: primary_email, keycloak_user_id, frappe_user
├── Profile: first_name, last_name, mobile_no
├── Privacy: is_minor (COPPA), consent_captured, consent_timestamp
├── Membership: personal_org → Organization (auto-created at signup)
└── Status: Active/Inactive/Merged with source tracking
```

**Strengths:**

- Unified identity with Keycloak SSO integration
- COPPA support via `is_minor` flag
- Personal Organization auto-created at signup for private identity
- Clean invitation flow with stub creation and merge handling
- Permission propagation via Org Member + User Permission pattern

### 1.3 Keycloak + Frappe Auth Integration

**Strengths:**

- Enterprise-grade identity management
- SSO support out of the box
- MFA enforcement configurable per org
- Clean session sync via Python adapter
- Token refresh handling specified

### 1.4 Offline Sync Protocol

The architecture references `offline_real_time_sync_spec.md` which defines a comprehensive sync protocol:

```
Change Feeds (/sync.feed) → Write Queues (/sync.upsert_batch) → Conflict Resolution → Socket.IO Deltas
```

**Strengths:**

- Three conflict strategies: AI Smart Merge (primary), Human Fallback (secondary), Last-Write-Wins (audit)
- Tombstones for delete tracking (30-day delta retention)
- Batch upsert with per-item response status
- Pagination with `has_more` + `next_since` watermarks
- Exponential backoff on errors
- Observability: queue depth, conflict rate, lag metrics
- Permission enforcement across REST, Socket.IO, and background jobs

### 1.5 Module/Plugin System

**Strengths:**

- Frappe app structure leveraged correctly
- Module discovery API for Flutter client
- Feature flags per organization
- Supports vertical modules (Fax, Family, Legal, Company)

---

## Part 2: Critical Gaps & Concerns

### 2.1 Offline Sync Conflict Resolution - ✅ RESOLVED

> **Resolution:** Per-DocType conflict strategies added to `offline_real_time_sync_spec.md`. See the "Per-DocType Conflict Strategies" section.

**Original Issue (Downgraded from Critical to Medium):**

**Problem:** The sync spec defines three conflict strategies (AI Merge, Human Fallback, LWW) but **lacks per-DocType strategy assignments**.

**What's Defined (in `offline_real_time_sync_spec.md`):**
- ✅ AI Smart Merge as primary strategy
- ✅ Human Fallback UI workflow (side-by-side diff, field-level picker)
- ✅ Last-Write-Wins for "low-value, high-velocity data"
- ✅ Tombstones always win over updates

**What's Missing:**

```python
# The sync spec doesn't specify:
# - Which DocTypes use AI Merge vs Human Fallback vs LWW?
# - What constitutes "sensitive doctypes" requiring human resolution?
# - Which fields are "low-value, high-velocity"?
# - Per-field merge rules for complex DocTypes (Task, Calendar Event)
```

**Impact:** Without per-DocType assignments, developers must make ad-hoc decisions leading to:

- Inconsistent UX (some conflicts auto-merge, others prompt)
- Potential data loss if wrong strategy selected
- AI Merge costs for DocTypes that don't need it

**Recommendation:**

```python
# Add to architecture: conflict_resolution_strategies.py

CONFLICT_STRATEGIES = {
    # Core DocTypes
    "Task": {
        "strategy": "field_level",
        "server_wins": ["status", "assigned_to"],
        "client_wins": ["notes"],
        "last_write_wins": ["title", "description"],
    },

    "Person": {
        "strategy": "server_wins",
        "reason": "Identity data is authoritative on server",
    },

    "Calendar Event": {
        "strategy": "manual_resolve",
        "reason": "Time conflicts require human decision",
        "auto_merge_fields": ["notes", "description"],
    },

    "Notification": {
        "strategy": "client_wins",
        "reason": "Read state is user-local",
    },

    # Default for unlisted DocTypes
    "_default": {
        "strategy": "server_wins",
    },
}
```

**Severity:** 🟡 Medium - Should define before implementing sync features

---

### 2.2 AI Infrastructure Details - HIGH

**Problem:** The PRD defines extensive AI features (Section 12) but architecture lacks implementation details.

**PRD Requirements:**

- AI Persona System with tool execution
- Document AI (OCR, classification, entity extraction)
- Voice interface with speech-to-text
- Knowledge Vault with RAG
- Local LLM support (Ollama)

**What's Missing:**

1. **LLM Provider Configuration:**

   - How are API keys stored securely?
   - How is provider failover handled?
   - What's the rate limiting strategy per org?

2. **Knowledge Vault Implementation:**

   - Vector database choice (pgvector? Pinecone? Weaviate?)
   - Embedding model and chunking strategy
   - Index refresh and invalidation

3. **Tool Execution Security:**
   - How are tool permissions enforced?
   - What's the audit trail for AI-triggered actions?
   - How is prompt injection prevented?

**Recommendation:**

```python
# Add to architecture: ai_infrastructure.py

AI_CONFIG = {
    "providers": {
        "openai": {
            "key_storage": "frappe.conf or Vault",
            "rate_limit_per_org": 1000,  # requests/hour
            "fallback_to": "anthropic",
        },
        "local": {
            "type": "ollama",
            "base_url": "http://localhost:11434",
            "models": ["llama3:8b", "mistral:7b"],
        },
    },

    "knowledge_vault": {
        "vector_db": "pgvector",  # In-database for simplicity
        "embedding_model": "text-embedding-3-small",
        "chunk_size": 512,
        "chunk_overlap": 50,
        "max_results": 5,
    },

    "tool_execution": {
        "audit_all": True,
        "permission_check": "before_execution",
        "timeout_seconds": 30,
        "sandbox_mode": "per_org_setting",
    },
}
```

**Severity:** 🟠 High - Blocks AI feature implementation

---

### 2.3 Integration OAuth Token Lifecycle - ✅ RESOLVED

> **Resolution:** Full token lifecycle specification created in `integration_token_management_spec.md`. Includes TokenManager class, encryption strategy, proactive refresh scheduler, and admin notifications.

**Original Issue (High Priority):**

**Problem:** PRD defines 40+ integrations (Section 11) but architecture lacks token lifecycle management.

**PRD Requirements:**

- C-15: Pre-Built Integrations Marketplace
- OAuth2 connections with token refresh
- Credential storage (encrypted)
- Connection health monitoring

**What's Missing:**

1. **Token Refresh Orchestration:**

   - How are tokens proactively refreshed before expiry?
   - What happens when refresh fails?
   - How are race conditions prevented?

2. **Credential Encryption:**

   - Which encryption scheme (AES-256-GCM)?
   - Where are keys stored (KMS, Vault)?
   - How is key rotation handled?

3. **Connection Health:**
   - How often are connections checked?
   - What constitutes "unhealthy"?
   - How are users notified of expired connections?

**Recommendation:**

```python
# Add to architecture: integration_token_manager.py

class TokenManager:
    """
    Centralized OAuth token management with proactive refresh.
    """

    REFRESH_BUFFER_SECONDS = 300  # Refresh 5 min before expiry

    @classmethod
    def get_access_token(cls, integration: str, organization: str) -> str:
        """
        Get valid access token, refreshing if needed.
        Thread-safe with per-token locking.
        """
        token_doc = cls._get_token_doc(integration, organization)

        if cls._needs_refresh(token_doc):
            token_doc = cls._refresh_token(token_doc)

        return token_doc.access_token

    @classmethod
    def _refresh_token(cls, token_doc):
        """Refresh with error handling and notification."""
        try:
            new_tokens = provider.refresh_access_token(token_doc.refresh_token)
            token_doc.update(new_tokens)
            token_doc.save()
        except RefreshTokenExpiredError:
            token_doc.status = "Expired"
            token_doc.save()
            cls._notify_admins_reconnection_needed(token_doc)
            raise IntegrationReauthRequiredError()


# Scheduled job: Proactive refresh
scheduler_events = {
    "cron": {
        "*/5 * * * *": ["dartwing_core.integrations.proactive_token_refresh"]
    }
}
```

**Severity:** 🟠 High - Integrations will fail unpredictably without this

---

### 2.4 Socket.IO Horizontal Scaling - ✅ RESOLVED

> **Resolution:** Full specification created in `socket_io_scaling_spec.md`. Includes Redis pub/sub adapter pattern, Python-side patches, Node.js configuration, and room naming conventions.

**Original Issue (High Priority):**

**Problem:** Frappe's Socket.IO runs single-node. PRD requires real-time features at scale.

**PRD Requirements:**

- C-04: Real-Time Collaboration
- Notifications across devices
- Multi-org real-time updates

**What's Missing:**

The architecture doesn't address:

- How Socket.IO scales across multiple server nodes
- How messages reach users connected to different nodes
- How rooms are synchronized across nodes

**Impact:** With multiple web servers:

```
User A (Server 1) publishes to room "org_123"
User B (Server 2) is in room "org_123" but NEVER receives the message
```

**Recommendation:**

```python
# Add to architecture: socket_io_scaling.py

"""
Socket.IO Horizontal Scaling via Redis Adapter
"""

# 1. Python side: Publish to Redis instead of local Socket.IO
def publish_realtime_via_redis(event, message, room):
    redis_client.publish("frappe:realtime", json.dumps({
        "event": event,
        "message": message,
        "room": room,
    }))

# 2. Node.js side: Use Redis adapter
# In frappe/socketio.js:
# const { createAdapter } = require("@socket.io/redis-adapter");
# io.adapter(createAdapter(pubClient, subClient));

# 3. Deployment: Use sticky sessions + Redis pub/sub
# nginx: ip_hash for sticky sessions
# Each Socket.IO node subscribes to Redis channel
```

**Severity:** 🟠 High - Real-time features will fail at scale

---

### 2.5 Observability Infrastructure - ✅ RESOLVED

> **Resolution:** Full specification created in `observability_spec.md`. Includes HTTP/job/database/integration metrics, structured logging format, alert definitions, and dashboard requirements.

**Original Issue (Medium Priority):**

**Problem:** Observability is partially defined but not comprehensive across all subsystems.

**What's Defined (in `offline_real_time_sync_spec.md`):**
- ✅ Sync metrics: queue depth, conflict rate, 5xx rate, delta size, lag
- ✅ Logs: per-request trace ID, org + doctype for audit, error logs with reasons
- ✅ Alerts: spike in conflicts, sustained lag > 5 minutes, failure to advance watermark

**What's Missing (for full production readiness):**

1. **HTTP/API Metrics:**
   - Request latency (p50, p95, p99) by endpoint
   - Error rates by endpoint/method
   - Rate limiting metrics

2. **Infrastructure Metrics:**
   - Database connection pool utilization
   - Redis connection health
   - Worker process health

3. **Logging Standardization:**
   - Structured logging format for all subsystems (not just sync)
   - Log aggregation strategy (Loki, CloudWatch, etc.)
   - Retention policy for compliance

4. **Alerting Coverage:**
   - Background job queue depth alerts
   - Integration health alerts
   - Auth failure rate alerts

**Recommendation:**

```python
# Add to architecture: observability.py

METRICS = {
    "http": {
        "request_duration_seconds": {
            "type": "histogram",
            "buckets": [0.01, 0.05, 0.1, 0.5, 1, 5],
            "labels": ["method", "endpoint", "status"],
        },
        "request_total": {
            "type": "counter",
            "labels": ["method", "endpoint", "status"],
        },
    },
    "background_jobs": {
        "queue_depth": {"type": "gauge", "labels": ["queue"]},
        "job_duration_seconds": {"type": "histogram", "labels": ["job_type"]},
        "job_failures_total": {"type": "counter", "labels": ["job_type"]},
    },
    "database": {
        "query_duration_seconds": {"type": "histogram"},
        "connection_pool_size": {"type": "gauge"},
    },
}

LOGGING = {
    "format": "json",
    "level": "INFO",
    "aggregator": "Loki or CloudWatch",
    "retention_days": 90,
}

ALERTING = {
    "critical": {
        "error_rate_5xx > 1%": {"for": "5m", "channel": "pagerduty"},
        "p99_latency > 5s": {"for": "10m", "channel": "pagerduty"},
    },
    "warning": {
        "queue_depth > 1000": {"for": "15m", "channel": "slack"},
        "error_rate_5xx > 0.1%": {"for": "15m", "channel": "slack"},
    },
}
```

**Severity:** 🟡 Medium - Operations will struggle without this

---

### 2.6 Multi-Tenant Permission Performance - MEDIUM

**Problem:** Every query requires organization filtering. At scale, this impacts performance.

**PRD Requirements:**

- C-03: Multi-Organization Management
- C-17: Role & Permission System
- Users may belong to 10+ organizations

**What's Missing:**

1. **Permission Query Optimization:**

   - How are user→org mappings cached?
   - How are permission checks batched?
   - What indexes are required?

2. **Cross-Org Query Pattern:**
   - How does a user query across multiple orgs efficiently?
   - How is the "All Organizations" view implemented?

**Recommendation:**

```python
# Add to architecture: permission_optimization.py

# 1. Cache user's organizations (invalidate on membership change)
def get_user_organizations(user: str) -> list[str]:
    cache_key = f"user_orgs:{user}"
    cached = frappe.cache().get_value(cache_key)
    if cached:
        return cached

    orgs = frappe.get_all(
        "Org Member",
        filters={"user": user, "status": "Active"},
        pluck="organization"
    )

    frappe.cache().set_value(cache_key, orgs, expires_in_sec=300)
    return orgs

# 2. Required indexes for permission queries
REQUIRED_INDEXES = [
    ("tabTask", ["organization", "status"]),
    ("tabTask", ["organization", "assigned_to", "status"]),
    ("tabPerson", ["organization"]),
    ("tabOrg Member", ["user", "status"]),
]

# 3. Batch permission check for list views
def check_permissions_batch(doctype: str, names: list[str]) -> dict[str, bool]:
    """Check read permission for multiple docs in one query."""
    # Implementation
```

**Severity:** 🟡 Medium - Performance degrades with org count

---

### 2.7 Compliance Mode Implementation - MEDIUM

**Problem:** PRD defines HIPAA/SOC2/GDPR modes but architecture lacks enforcement details.

**PRD Requirements:**

- C-13: Compliance-Ready Mode (one-toggle enablement)
- C-20: Immutable Audit Trail
- C-21: Data Residency Selection

**What's Missing:**

1. **HIPAA Mode Enforcement:**

   - Which controls are activated?
   - How is PHI tagging enforced?
   - What's the audit log format?

2. **Immutable Storage:**
   - How is S3 Object Lock configured?
   - How is chain integrity verified?
   - How are audit logs queried?

**Recommendation:**

```python
# Add to architecture: compliance_enforcement.py

HIPAA_CONTROLS = {
    "access": {
        "session_timeout_minutes": 15,
        "mfa_required": True,
        "password_min_length": 12,
    },
    "audit": {
        "log_all_phi_access": True,
        "immutable_storage": "s3_object_lock",
        "retention_years": 7,
    },
    "encryption": {
        "at_rest": "AES-256",
        "in_transit": "TLS-1.3",
        "key_management": "AWS-KMS",
    },
}

def enable_hipaa_mode(organization: str):
    """Activate all HIPAA controls for an organization."""
    org = frappe.get_doc("Organization", organization)
    org.hipaa_mode = True
    org.session_timeout = HIPAA_CONTROLS["access"]["session_timeout_minutes"]
    org.mfa_required = True
    org.save()

    # Activate audit trail
    enable_phi_audit_logging(organization)

    # Configure immutable storage
    configure_s3_object_lock(organization)
```

**Severity:** 🟡 Medium - Compliance features won't work correctly

---

### 2.8 Background Job Isolation - ✅ RESOLVED

> **Resolution:** Full specification created in `background_job_isolation_spec.md`. Includes queue hierarchy (critical/default/bulk), per-org job limits, DLQ pattern, retry strategies, and permission enforcement in async context.

**Original Issue (Medium Priority):**

**Problem:** PRD mentions background jobs but architecture doesn't address noisy neighbor issues.

**PRD Requirements:**

- C-09: Background Job System
- Multi-tenant with potentially large orgs
- SLA-bound operations (fax, notifications)

**What's Missing:**

1. **Queue Isolation:**

   - How are critical jobs prioritized?
   - How is one org prevented from starving others?
   - What's the retry strategy?

2. **Job Monitoring:**
   - How are stuck jobs detected?
   - What's the dead letter queue strategy?
   - How are job failures alerted?

**Recommendation:**

```python
# Add to architecture: job_queue_strategy.py

QUEUE_CONFIG = {
    "critical": {
        "workers": 4,
        "max_jobs_per_org": 100,
        "timeout_seconds": 60,
        "doctypes": ["Fax Job", "Notification"],
    },
    "default": {
        "workers": 8,
        "max_jobs_per_org": 500,
        "timeout_seconds": 300,
    },
    "bulk": {
        "workers": 2,
        "rate_limit_per_minute": 100,
        "doctypes": ["Bulk Import", "Report Generation"],
    },
}

# Dead letter queue
DLQ_CONFIG = {
    "max_retries": 3,
    "retry_delay_seconds": [60, 300, 900],  # Exponential backoff
    "dlq_retention_days": 7,
    "alert_on_dlq_depth": 50,
}
```

**Severity:** 🟡 Medium - Operations will degrade under load

---

## Part 3: PRD Feature Implementation Feasibility

### 3.1 Feature Risk Matrix

| Feature                 | PRD Ref | Architecture Support | Risk      | Notes                            |
| ----------------------- | ------- | -------------------- | --------- | -------------------------------- |
| Multi-Org Management    | C-03    | ✅ Strong            | 🟢 Low    | Well-designed                    |
| Real-Time Collaboration | C-04    | ⚠️ Partial           | 🟠 High   | Socket.IO scaling gap            |
| Task Management         | C-05    | ✅ Strong            | 🟢 Low    | Standard CRUD                    |
| Calendar                | C-08    | ⚠️ Partial           | 🟡 Medium | Per-DocType conflict rules needed|
| Background Jobs         | C-09    | ⚠️ Partial           | 🟡 Medium | Isolation needed                 |
| Offline-First           | C-10    | ✅ Good              | 🟡 Medium | Strategies defined; rules needed |
| Notifications           | C-11    | ✅ Strong            | 🟢 Low    | Well-specified                   |
| Fax Engine              | C-12    | ✅ Strong            | 🟢 Low    | Separate module                  |
| Compliance Mode         | C-13    | ⚠️ Partial           | 🟡 Medium | Enforcement details missing      |
| Plugin System           | C-14    | ✅ Strong            | 🟢 Low    | Frappe-native                    |
| Integrations            | C-15    | ⚠️ Partial           | 🟠 High   | Token management gap             |
| Permission System       | C-17    | ✅ Strong            | 🟢 Low    | Frappe-native + enhancements     |
| Immutable Audit         | C-20    | ⚠️ Partial           | 🟡 Medium | Implementation details missing   |
| Data Residency          | C-21    | ⚠️ Partial           | 🟡 Medium | Enforcement needed               |
| Feature Flags           | C-22    | ✅ Strong            | 🟢 Low    | Well-specified                   |
| AI Personas             | S12     | ⚠️ Weak              | 🔴 High   | Infrastructure missing           |
| Document AI             | S12     | ⚠️ Weak              | 🔴 High   | Pipeline not specified           |
| Voice Interface         | S12     | ⚠️ Weak              | 🔴 High   | Not in architecture              |
| Knowledge Vault         | S12     | ⚠️ Weak              | 🔴 High   | Vector DB not specified          |
| Developer Portal        | S13     | ✅ Strong            | 🟢 Low    | Standard implementation          |
| Data Export             | S13     | ✅ Strong            | 🟢 Low    | Frappe-native                    |

### 3.2 Implementation Sequence Recommendation

```
Phase 1: Core Foundation (Weeks 1-8)
├─ Multi-Org Management (C-03) - Architecture ready
├─ Permission System (C-17) - Add caching layer
├─ Task Management (C-05) - Standard implementation
├─ Notifications (C-11) - Architecture ready
├─ Plugin System (C-14) - Frappe-native
└─ Offline-First (C-10) - Sync spec ready, add per-DocType rules

Phase 2: Real-Time & Scale (Weeks 9-14)
├─ Add Socket.IO Redis adapter - BLOCKER
├─ Real-Time Collaboration (C-04)
├─ Calendar (C-08) - Define conflict rules
└─ Full-stack observability

Phase 3: Integrations (Weeks 15-22)
├─ Add token manager - BLOCKER
├─ Integrations Marketplace (C-15)
├─ Background Job Isolation
└─ Developer Portal (S13)

Phase 4: Compliance (Weeks 23-30)
├─ Add compliance enforcement - BLOCKER
├─ Compliance Mode (C-13)
├─ Immutable Audit (C-20)
└─ Data Residency (C-21)

Phase 5: AI Features (Weeks 31-42)
├─ Add AI infrastructure - BLOCKER
├─ AI Personas
├─ Document AI
├─ Knowledge Vault
└─ Voice Interface (optional)
```

---

## Part 4: Technical Deep Dive - Recommended Solutions

### 4.1 Conflict Resolution Strategy Engine

```python
# dartwing_core/sync/conflict_engine.py

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable

class ConflictStrategy(Enum):
    SERVER_WINS = "server_wins"
    CLIENT_WINS = "client_wins"
    LAST_WRITE_WINS = "last_write_wins"
    FIELD_LEVEL = "field_level"
    MANUAL_RESOLVE = "manual_resolve"
    APPEND_ONLY = "append_only"


@dataclass
class ConflictRule:
    strategy: ConflictStrategy
    server_wins_fields: list[str] = None
    client_wins_fields: list[str] = None
    merge_function: Optional[Callable] = None


CONFLICT_RULES: dict[str, ConflictRule] = {
    # Core DocTypes
    "Organization": ConflictRule(
        strategy=ConflictStrategy.SERVER_WINS,
    ),

    "Person": ConflictRule(
        strategy=ConflictStrategy.SERVER_WINS,
    ),

    "Task": ConflictRule(
        strategy=ConflictStrategy.FIELD_LEVEL,
        server_wins_fields=["status", "assigned_to", "priority"],
        client_wins_fields=["notes", "attachments"],
    ),

    "Calendar Event": ConflictRule(
        strategy=ConflictStrategy.MANUAL_RESOLVE,
    ),

    "Notification": ConflictRule(
        strategy=ConflictStrategy.CLIENT_WINS,
    ),

    "Comment": ConflictRule(
        strategy=ConflictStrategy.APPEND_ONLY,
    ),
}


def resolve_conflict(
    doctype: str,
    local_doc: dict,
    server_doc: dict,
    ancestor_doc: dict,
) -> tuple[dict, bool]:
    """
    Resolve sync conflict using configured strategy.

    Returns:
        (merged_doc, needs_manual_resolution)
    """
    rule = CONFLICT_RULES.get(doctype, ConflictRule(
        strategy=ConflictStrategy.SERVER_WINS
    ))

    if rule.strategy == ConflictStrategy.SERVER_WINS:
        return server_doc, False

    elif rule.strategy == ConflictStrategy.CLIENT_WINS:
        return local_doc, False

    elif rule.strategy == ConflictStrategy.LAST_WRITE_WINS:
        if local_doc.get("modified") > server_doc.get("modified"):
            return local_doc, False
        return server_doc, False

    elif rule.strategy == ConflictStrategy.FIELD_LEVEL:
        merged = {}
        for field in set(local_doc.keys()) | set(server_doc.keys()):
            if field in rule.server_wins_fields:
                merged[field] = server_doc.get(field)
            elif field in rule.client_wins_fields:
                merged[field] = local_doc.get(field)
            else:
                # Default to server for unlisted fields
                merged[field] = server_doc.get(field)
        return merged, False

    elif rule.strategy == ConflictStrategy.MANUAL_RESOLVE:
        return None, True

    elif rule.strategy == ConflictStrategy.APPEND_ONLY:
        # Union of items (for list fields)
        return _merge_append_only(local_doc, server_doc, ancestor_doc), False

    return server_doc, False


def _merge_append_only(local: dict, server: dict, ancestor: dict) -> dict:
    """Merge using append-only semantics (union of additions)."""
    # Implementation for append-only merge
    merged = server.copy()

    # Find items added locally that aren't in server
    for key, value in local.items():
        if isinstance(value, list):
            ancestor_items = set(ancestor.get(key, []))
            local_added = set(value) - ancestor_items
            server_items = set(merged.get(key, []))
            merged[key] = list(server_items | local_added)

    return merged
```

### 4.2 Integration Token Manager

```python
# dartwing_core/integrations/token_manager.py

import threading
from datetime import timedelta
from cryptography.fernet import Fernet
import frappe
from frappe.utils import now_datetime


class TokenManager:
    """
    Centralized OAuth token management with:
    - Proactive refresh before expiry
    - Thread-safe per-token locking
    - Encrypted credential storage
    - Admin notification on auth failure
    """

    REFRESH_BUFFER_SECONDS = 300  # Refresh 5 min before expiry
    _locks: dict[str, threading.Lock] = {}
    _encryption_key: bytes = None

    @classmethod
    def get_access_token(
        cls,
        integration: str,
        organization: str,
    ) -> str:
        """Get valid access token, refreshing if needed."""
        token_key = f"{integration}:{organization}"

        # Get or create lock for this token
        if token_key not in cls._locks:
            cls._locks[token_key] = threading.Lock()

        with cls._locks[token_key]:
            token_doc = cls._get_token_doc(integration, organization)

            if not token_doc:
                raise IntegrationNotConnectedError(
                    f"{integration} not connected for this organization"
                )

            if cls._needs_refresh(token_doc):
                token_doc = cls._refresh_token(token_doc)

            return cls._decrypt(token_doc.access_token)

    @classmethod
    def _needs_refresh(cls, token_doc) -> bool:
        """Check if token needs refresh."""
        if not token_doc.expires_at:
            return False

        threshold = now_datetime() + timedelta(
            seconds=cls.REFRESH_BUFFER_SECONDS
        )
        return token_doc.expires_at <= threshold

    @classmethod
    def _refresh_token(cls, token_doc):
        """Refresh token with error handling."""
        provider = get_integration_provider(token_doc.integration)

        try:
            refresh_token = cls._decrypt(token_doc.refresh_token)
            new_tokens = provider.refresh_access_token(refresh_token)

            token_doc.access_token = cls._encrypt(new_tokens["access_token"])
            token_doc.expires_at = now_datetime() + timedelta(
                seconds=new_tokens.get("expires_in", 3600)
            )

            if "refresh_token" in new_tokens:
                token_doc.refresh_token = cls._encrypt(new_tokens["refresh_token"])

            token_doc.last_refreshed = now_datetime()
            token_doc.status = "Connected"
            token_doc.error_message = None
            token_doc.save(ignore_permissions=True)
            frappe.db.commit()

            return token_doc

        except RefreshTokenExpiredError:
            token_doc.status = "Expired"
            token_doc.error_message = "Refresh token expired - reconnection required"
            token_doc.save(ignore_permissions=True)
            frappe.db.commit()

            cls._notify_reconnection_needed(token_doc)
            raise IntegrationReauthRequiredError(
                f"{token_doc.integration} requires reconnection"
            )

    @classmethod
    def _encrypt(cls, value: str) -> str:
        """Encrypt credential value."""
        if cls._encryption_key is None:
            cls._encryption_key = cls._get_encryption_key()

        f = Fernet(cls._encryption_key)
        return f.encrypt(value.encode()).decode()

    @classmethod
    def _decrypt(cls, encrypted: str) -> str:
        """Decrypt credential value."""
        if cls._encryption_key is None:
            cls._encryption_key = cls._get_encryption_key()

        f = Fernet(cls._encryption_key)
        return f.decrypt(encrypted.encode()).decode()

    @classmethod
    def _get_encryption_key(cls) -> bytes:
        """Get encryption key from secure storage."""
        # Option 1: From frappe.conf
        key = frappe.conf.get("integration_encryption_key")
        if key:
            return key.encode()

        # Option 2: From environment
        key = os.environ.get("DARTWING_INTEGRATION_KEY")
        if key:
            return key.encode()

        # Option 3: Generate and store (first-time setup)
        key = Fernet.generate_key()
        # Store in secure location
        return key

    @classmethod
    def _notify_reconnection_needed(cls, token_doc):
        """Notify org admins that integration needs reconnection."""
        admins = frappe.get_all(
            "Org Member",
            filters={
                "organization": token_doc.organization,
                "role": "Admin",
            },
            pluck="user"
        )

        for admin in admins:
            frappe.publish_realtime(
                "integration_expired",
                {
                    "integration": token_doc.integration,
                    "message": f"{token_doc.integration} connection expired. Please reconnect.",
                },
                user=admin
            )


# Scheduled job: Proactive token refresh
def proactive_token_refresh():
    """
    Run every 5 minutes to refresh tokens BEFORE they expire.
    Prevents request failures due to token expiry.
    """
    expiring_soon = frappe.get_all(
        "Organization Integration",
        filters={
            "status": "Connected",
            "expires_at": ["<=", now_datetime() + timedelta(minutes=10)]
        },
        fields=["name", "integration", "organization"]
    )

    for token in expiring_soon:
        try:
            TokenManager.get_access_token(
                token.integration,
                token.organization
            )
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(
                f"Proactive refresh failed: {token.integration}",
                str(e)
            )
```

### 4.3 Socket.IO Redis Adapter

```python
# dartwing_core/realtime/redis_adapter.py

"""
Socket.IO Horizontal Scaling via Redis Adapter

This module patches Frappe's publish_realtime to use Redis pub/sub,
enabling Socket.IO messages to reach users on any server node.
"""

import json
import redis
import frappe


def get_redis_client():
    """Get Redis client for Socket.IO pub/sub."""
    redis_url = frappe.conf.get("redis_socketio") or frappe.conf.get("redis_cache")
    return redis.from_url(redis_url)


def patch_frappe_realtime():
    """
    Monkey-patch frappe.publish_realtime to use Redis pub/sub.
    Call this on app startup via hooks.py app_include_js or on_startup.
    """
    import frappe.realtime

    original_publish = frappe.realtime.publish_realtime

    def redis_publish_realtime(
        event,
        message=None,
        room=None,
        user=None,
        doctype=None,
        docname=None,
        after_commit=True
    ):
        """Enhanced publish that goes through Redis for cross-node delivery."""
        if after_commit:
            frappe.db.after_commit.add(
                lambda: _redis_emit(event, message, room, user, doctype, docname)
            )
        else:
            _redis_emit(event, message, room, user, doctype, docname)

    def _redis_emit(event, message, room, user, doctype, docname):
        redis_client = get_redis_client()

        payload = {
            "event": event,
            "message": message,
            "room": room,
            "user": user,
            "doctype": doctype,
            "docname": docname,
        }

        # Publish to Redis channel that all Socket.IO nodes subscribe to
        redis_client.publish("dartwing:realtime", json.dumps(payload))

    frappe.realtime.publish_realtime = redis_publish_realtime


# hooks.py configuration
# app_include_js = ["dartwing_core/realtime/redis_adapter.patch_frappe_realtime"]
```

**Node.js Socket.IO Configuration:**

```javascript
// frappe-bench/apps/dartwing_core/socketio_patch.js

const { createAdapter } = require("@socket.io/redis-adapter");
const { createClient } = require("redis");

async function setupRedisAdapter(io) {
  const redisUrl = process.env.REDIS_SOCKETIO_URL || "redis://localhost:6379";

  const pubClient = createClient({ url: redisUrl });
  const subClient = pubClient.duplicate();

  await Promise.all([pubClient.connect(), subClient.connect()]);

  io.adapter(createAdapter(pubClient, subClient));

  console.log("Socket.IO Redis adapter connected");

  // Subscribe to Python-published messages
  const messageClient = pubClient.duplicate();
  await messageClient.connect();

  await messageClient.subscribe("dartwing:realtime", (message) => {
    const payload = JSON.parse(message);

    if (payload.room) {
      io.to(payload.room).emit(payload.event, payload.message);
    } else if (payload.user) {
      io.to(`user:${payload.user}`).emit(payload.event, payload.message);
    } else if (payload.doctype && payload.docname) {
      io.to(`doc:${payload.doctype}:${payload.docname}`).emit(
        payload.event,
        payload.message
      );
    }
  });
}

module.exports = { setupRedisAdapter };
```

---

## Part 5: Architecture Completeness Score

| Category             | Score (Before) | Score (After) | Notes                                                   |
| -------------------- | -------------- | ------------- | ------------------------------------------------------- |
| Multi-Tenancy        | 95%            | 95%           | Well-designed Organization model                        |
| Authentication       | 90%            | 90%           | Keycloak integration solid                              |
| Authorization        | 85%            | 85%           | Good base, needs caching optimization                   |
| Offline Sync         | 75%            | **95%**       | ✅ Per-DocType conflict strategies now defined          |
| Real-Time            | 50%            | **90%**       | ✅ Redis adapter pattern specified                      |
| AI Features          | 30%            | 30%           | High-level only, implementation missing (P2)            |
| Integrations         | 50%            | **90%**       | ✅ Full token lifecycle with encryption specified       |
| Compliance           | 60%            | 60%           | Requirements listed, enforcement missing (P2)           |
| Observability        | 45%            | **90%**       | ✅ Full-stack metrics, logging, alerting defined        |
| Background Jobs      | 40%            | **90%**       | ✅ Queue isolation, DLQ, retry strategies defined       |
| Developer Experience | 80%            | 80%           | API well-specified                                      |
| **Overall**          | **66%**        | **85%**       | Production-ready for core features; AI/Compliance P2    |

---

## Part 6: Recommendations Summary

### 6.1 Must-Do Before Production

| Priority | Gap                            | Effort  | Status | Resolution |
| -------- | ------------------------------ | ------- | ------ | ---------- |
| 🔴 P0    | Socket.IO Redis adapter        | 1 week  | ✅ DONE | `socket_io_scaling_spec.md` |
| 🔴 P0    | Integration token manager      | 2 weeks | ✅ DONE | `integration_token_management_spec.md` |
| 🟠 P1    | Per-DocType conflict rules     | 1 week  | ✅ DONE | Updated `offline_real_time_sync_spec.md` |
| 🟠 P1    | Observability (non-sync)       | 2 weeks | ✅ DONE | `observability_spec.md` |
| 🟠 P1    | Background job isolation       | 2 weeks | ✅ DONE | `background_job_isolation_spec.md` |
| 🟡 P2    | Permission query optimization  | 1 week  | ⏳ TODO | Deferred |
| 🟡 P2    | Compliance enforcement         | 2 weeks | ⏳ TODO | Deferred |

### 6.2 Defer to Post-MVP

| Feature              | Reason                          |
| -------------------- | ------------------------------- |
| AI Personas          | Complex, needs dedicated sprint |
| Document AI Pipeline | External dependencies           |
| Voice Interface      | Nice-to-have, not core          |
| Local LLM (Ollama)   | Privacy premium feature         |

### 6.3 Architecture Changes Needed

| Current                              | Recommended                          | Status |
| ------------------------------------ | ------------------------------------ | ------ |
| Single-node Socket.IO                | Redis adapter for horizontal scaling | ✅ Specified |
| Generic conflict strategies          | Per-DocType strategy assignments     | ✅ Specified |
| Direct API calls to integrations     | Centralized token manager            | ✅ Specified |
| Sync-only observability              | Full-stack observability             | ✅ Specified |
| No job isolation                     | Queue strategy with per-org limits   | ✅ Specified |

---

## Part 7: Conclusion

The Dartwing Core architecture provides a **solid foundation** built on proven technology (Frappe + Flutter + Keycloak). The multi-tenancy model, authentication, offline sync protocol, and basic CRUD operations are **production-ready**.

**Key strengths discovered on review:**
- Offline sync spec (`offline_real_time_sync_spec.md`) is more complete than initially assessed
- Three conflict strategies defined with clear fallback hierarchy
- Sync-specific observability already specified

**Gaps addressed in this iteration (all P0/P1 items resolved):**

1. ~~**Real-time scaling**~~ ✅ Redis adapter pattern specified (`socket_io_scaling_spec.md`)
2. ~~**Integration tokens**~~ ✅ Centralized token manager specified (`integration_token_management_spec.md`)
3. ~~**Per-DocType conflict rules**~~ ✅ Strategies assigned (updated `offline_real_time_sync_spec.md`)
4. ~~**Full-stack observability**~~ ✅ Complete spec created (`observability_spec.md`)
5. ~~**Job isolation**~~ ✅ Queue strategy specified (`background_job_isolation_spec.md`)

**Remaining P2 items for future iterations:**
- Permission query optimization
- Compliance enforcement details
- AI infrastructure

The PRD's 22+ features are **achievable** with the architecture specifications now in place. AI features (Section 12) require the most additional infrastructure work and should be sequenced after core platform stability.

**Architecture completeness improved from 66% to 85%.** Ready for implementation of core features.

---

_Critique prepared: November 2025_
_Updated: November 2025 (after specification work)_
_Reviewer: Claude (Opus 4.5)_
_Architecture version: Dartwing Core 1.0_
_PRD version: 1.0_
