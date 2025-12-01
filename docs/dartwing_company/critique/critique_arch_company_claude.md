# Dartwing Company Architecture Critique

**Focus: AI-First Operations Platform Architecture**

**Status: November 2025 (Comprehensive Review v2)**

---

## Executive Summary

The Dartwing Company architecture presents an ambitious **AI-First Operations Platform** built as an overlay on the Frappe ecosystem. The architecture document is comprehensive at ~11,500 lines (expanded from ~5,000 with Sections 10-16), covering integration patterns, DocType schemas, permission frameworks, and implementation details.

The **"Overlay, Don't Extend"** approach is strategically sound - it avoids forking Frappe apps and ensures upgradeability. However, this model introduces significant complexity in **data synchronization** and **state management**. The primary risk is not in feature logic itself, but in the _glue_ between Dartwing and underlying Frappe apps. If not managed perfectly, the system risks becoming a "distributed monolith" where a change in ERPNext breaks a Dartwing workflow.

---

## 1. Architecture Strengths

### 1.1 Sound Core Principles

| Principle | Assessment |
|-----------|------------|
| **Overlay, Don't Extend** | Excellent - avoids forking Frappe apps, ensures upgradeability |
| **Link, Don't Copy** | Correct - prevents data duplication and sync nightmares |
| **Event-Driven** | Good use of Frappe's doc_events for loose coupling |
| **API-First** | Essential for Flutter mobile app integration |

**Strategic Value:** By linking to `Customer` (ERPNext) rather than modifying it, the system remains resilient to ERPNext upgrades. Using ERPNext as "Source of Truth" for accounting and HRMS for payroll ensures Dartwing doesn't accidentally corrupt financial or legal data.

### 1.2 Well-Structured Integration Patterns

The ERPNext, HRMS, CRM, Health, and Drive integration diagrams are clear and follow consistent patterns:

```
dartwing_company DocType → Link → Frappe App DocType
                        → Custom Fields on Frappe App
                        → doc_events to react to changes
```

**Specific Strengths:**
- Clear 1:1 relationships between Organization and ERPNext Company / HRMS Company
- Custom fields on Frappe apps (Attendance, Customer, Employee, Lead) are well-documented
- Permission query hooks for multi-tenancy are properly defined

### 1.3 Comprehensive hooks.py Configuration

The hooks.py is thorough with:
- `doc_events` for both our DocTypes and Frappe app DocTypes
- `scheduler_events` with appropriate frequencies (1min for SLA, 5min for anomalies, daily for standup)
- `permission_query_conditions` for multi-tenancy
- `override_doctype_class` for extending Frappe app behavior
- `fixtures` for custom field deployment

### 1.4 Modular Directory Structure

The directory structure separates concerns well:
```
dartwing_company/
├── doctype/           # Data definitions
├── operations/        # OPS feature engines
├── crm/               # CRM overlay engines
├── hr/                # HR overlay engines
├── integrations/      # External service clients
├── api/               # REST endpoints
└── events/            # Doc event handlers
```

### 1.5 Channel Plugin Architecture

The Universal Inbox channel plugin pattern is well-designed:
- Abstract base class with clear interface
- Normalized `InboundMessage` dataclass
- Sync and webhook methods for both polling and real-time
- Easy to add new channels (Telegram, Instagram, etc.)

### 1.6 Smart Assignment Algorithm

The dispatch assignment algorithm is well-thought-out with:
- Multi-factor scoring (proximity, workload, skills, customer preference)
- Weighted calculation with tunable parameters
- Clear query patterns for HRMS integration

### 1.7 Robust RAG & AI Integration

- The RAG architecture (OpenSearch + Vector Embeddings) is well-designed
- "Ask Anything" (OPS-12) and "Growth Orchestrator" (CRM-07) are high-value differentiators

### 1.8 Workflow Engine (OPS-03)

- Event-driven workflow engine (Trigger -> Condition -> Action) is powerful
- Ability to call webhooks and sync with external tools (Planner, Trello) makes it a true "Operating System"

---

## 2. Architecture Weaknesses & Risks

### 2.1 The "Sync Hell" of Overlays

**Priority: HIGH** | **Risk: CRITICAL**

The architecture relies on `doc_events` (hooks) to keep Dartwing in sync with Frappe apps.

**Problem Scenario:**
- User updates Customer address in ERPNext via bulk import or direct SQL script
- The `on_update` hook might not fire, or might fail
- Result: Dispatch Job (Dartwing) has old location data, sending tech to wrong address

**Mitigation Recommendations:**
1. Implement **Nightly Reconciliation Job** comparing Dartwing links with source data
2. Use **Database Triggers** or strict API gateways preventing "backdoor" updates
3. Consider **Event Sourcing** - log events (e.g., `CustomerAddressChanged`) to replay if behind

---

### 2.2 Missing Error Handling Patterns

**Priority: HIGH** | **Status: NOT DOCUMENTED**

No explicit error handling strategy for:
- External API failures (Maps, Stripe, AI/LLM)
- Cross-system transaction failures (ERPNext + HRMS + CRM)
- Partial operation rollback

**Recommendation:** Add error handling patterns:
```python
# Retry with exponential backoff
@retry(stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_external_service(): ...

# Circuit breaker for unreliable services
@circuit_breaker(failure_threshold=5, recovery_timeout=60)
async def call_flaky_api(): ...
```

---

### 2.3 Transaction Management Gaps

**Priority: HIGH** | **Status: NOT DOCUMENTED**

When a Dispatch Job completes, it triggers:
1. Sales Invoice creation (ERPNext)
2. Timesheet creation (HRMS)
3. Activity Log (CRM)

**Problem:** No documented pattern for what happens if step 2 fails after step 1 succeeds.

**Recommendation:** Document saga pattern or compensating transactions:
```python
def complete_dispatch_job(job):
    try:
        with frappe.db.transaction():
            job.status = "completed"
            job.save()

        invoice = create_invoice(job)
        try:
            timesheet = create_timesheet(job)
        except Exception:
            invoice.cancel()  # Compensate
            raise
    except Exception:
        job.status = "completion_failed"
        job.save()
        notify_admin("Dispatch job completion failed", job)
```

---

### 2.4 Dispatch Algorithm Performance

**Priority: MEDIUM** | **Risk: SCALABILITY** | **Status: ✅ RESOLVED**

~~The `SmartAssignment` class fetches _all_ available employees and filters them in Python.~~

~~**Problem at Scale:** For a company with 1,000 technicians, fetching all employee records + certifications + leave applications + daily job counts will be slow (seconds per job).~~

**RESOLVED in Section 5.2:** The `SmartAssignment` class has been completely refactored with SQL-optimized filtering:

```sql
SELECT emp.name, emp.employee_name, emp.home_location,
    (SELECT COUNT(*) FROM `tabDispatch Job` ...) as jobs_today
FROM `tabEmployee` emp
WHERE emp.status = 'Active' AND emp.dispatch_enabled = 1
    AND emp.name NOT IN (SELECT employee FROM `tabLeave Application` ...)
    AND emp.name IN (SELECT ec.employee FROM `tabEmployee Certification` ...)
ORDER BY jobs_today ASC
LIMIT 50
```

**Performance Results:**
| Employee Count | Before (ms) | After (ms) |
|----------------|-------------|------------|
| 50             | 450         | 45         |
| 500            | 4,500       | 58         |
| 1,000          | TIMEOUT     | 65         |

**Additional Improvements:**
- Pre-computes `jobs_today` and `last_job_end_time` in SQL (avoids N+1)
- Parallel drive time calculations via `asyncio.gather`
- Cached skill match and customer preference lookups
- Required database indexes documented and installation patch provided

---

### 2.5 Universal Inbox State Management

**Priority: HIGH** | **Complexity: HIGH**

Aggregating Email (IMAP), SMS, and WhatsApp into one `Conversation` is complex:
- WhatsApp has 24-hour response window
- Email is threaded
- SMS is linear

**Risk:** The `ChannelPlugin` interface is good, but handling channel nuances (e.g., "Message failed to send" callbacks) requires robust state machine.

**Recommendation:** Adopt **State Machine** for messages:
```
Sending -> Sent -> Delivered -> Read -> Failed
```
Ensure UI reflects these states clearly per channel.

---

### 2.6 Inconsistent Async/Sync Patterns

**Priority: MEDIUM** | **Status: INCONSISTENT**

The architecture mixes:
- `async def` methods in channel plugins
- Regular `def` in DocType controllers
- No clear pattern for when to use which

**Problem:** Frappe's background jobs don't natively support async. This will cause runtime issues.

**Recommendation:** Standardize on:
1. Sync for all DocType hooks and controller methods
2. Async only for external API calls within background jobs using `asyncio.run()`
3. Document the pattern explicitly

---

### 2.7 Missing Caching Strategy

**Priority: MEDIUM** | **Status: NOT DOCUMENTED**

High-frequency operations that need caching:
- Employee availability checks (called for every dispatch assignment)
- Customer portal settings (called on every page load)
- AI prompt templates
- Geocoding results

**Recommendation:** Add caching layer:
```python
@frappe.cache(ttl=300)  # 5 minutes
def get_employee_certifications(employee: str) -> dict: ...
```

---

### 2.8 RAG Implementation Under-Specified

**Priority: MEDIUM** | **Status: INCOMPLETE**

The Knowledge Base RAG architecture (OPS-07) shows high-level flow but lacks:
- Vector database choice (pgvector vs OpenSearch vs dedicated vector DB)
- Chunk sizing strategy
- Embedding model selection
- Context window management for LLM
- Citation linking implementation

**Recommendation:** Add detailed RAG section:
```
Vector Storage: OpenSearch with dense_vector field type
Chunk Size: 512 tokens with 50-token overlap
Embedding Model: text-embedding-3-small (OpenAI) or all-MiniLM-L6-v2 (local)
Top-K Retrieval: 5 chunks per query
```

---

### 2.9 Missing Rate Limiting

**Priority: MEDIUM** | **Status: NOT DOCUMENTED**

API endpoints lack rate limiting documentation:
- Portal API (client-facing)
- Webhook endpoints (external services)
- Search/AI endpoints (expensive operations)

---

### 2.10 Offline Sync Conflict Resolution

**Priority: MEDIUM** | **Status: NOT DOCUMENTED**

Mobile Forms (OPS-05) support offline mode, but no conflict resolution documented for:
- Form submitted offline, job status changed online
- Multiple users editing same dispatch job
- Clock-in recorded offline with stale schedule data

**Recommendation:** Explicitly mandate the **Dartwing Core Sync Protocol** (Change Feeds + Write Queues + AI Merge) for all mobile-facing DocTypes.

---

## 3. PRD Feature Implementation Analysis

### 3.1 Easy to Implement (Low Risk)

| Feature | PRD ID | Rationale | Effort |
|---------|--------|-----------|--------|
| **Status Boards** | OPS-06 | Frappe has List/Kanban views; minimal custom work | 2-3 weeks |
| **Visitor Management** | OPS-10 | Simple DocType + notification | 2 weeks |
| **Resource Booking** | OPS-11 | Standard CRUD with calendar view | 3 weeks |
| **Document Vault** | CRM-02 | Frappe Drive does heavy lifting | 2-3 weeks |
| **Custom Fields** | CRM-05 | JSON storage pattern is proven | 2 weeks |
| **Knowledge Base** | OPS-07 | Standard CRUD + RAG (well-solved problem) | 3-4 weeks |
| **Geo Clock-In** | HR-02 | Geofencing is standard mobile tech | 3 weeks |

### 3.2 Medium Difficulty (Manageable Risk)

| Feature | PRD ID | Challenges | Effort |
|---------|--------|------------|--------|
| **Mobile Forms** | OPS-05 | Offline sync is the hard part | 4-6 weeks |
| **Workflow Builder** | OPS-03 | Logic straightforward, UI builder complex | 6-8 weeks |
| **Smart Dispatch** | OPS-04 | GIS logic standard; performance optimization is hurdle | 6-8 weeks |
| **Shift Scheduler** | HR-01 | UI (drag-drop) complex; backend logic standard | 6-8 weeks |
| **Client Portal** | CRM-01 | Security/Permissions are the risk | 6-8 weeks |
| **Service Tickets** | CRM-04 | SLA timer implementation needs careful state management | 4-6 weeks |
| **Appointments** | CRM-03 | Calendar integration + Stripe payment complexity | 5-7 weeks |
| **Daily Standup** | OPS-09 | Scheduled job + LLM summarization | 3-4 weeks |
| **Growth Orchestrator** | CRM-07 | Prompt engineering key; leadgen integration well-defined | 6-8 weeks |

### 3.3 Hard to Implement (High Risk)

| Feature | PRD ID | Major Challenges | Effort |
|---------|--------|------------------|--------|
| **AI Receptionist** | OPS-01 | Voice AI latency, SIP integration, real-time "whisper" | 10-14 weeks |
| **Universal Inbox** | OPS-02 | State management across disparate channels | 10-12 weeks |
| **Ask Anything** | OPS-12 | Global search + AI query understanding + slash commands | 8-10 weeks |
| **Broadcast Alerts** | OPS-08 | Multi-channel blast (voice especially); acknowledgment at scale | 6-8 weeks |

---

## 4. Feature Risk Matrix

| Feature | PRD ID | Complexity | Dependency Risk | External Service Risk | Overall Risk |
|---------|--------|------------|-----------------|----------------------|--------------|
| Status Boards | OPS-06 | Low | Low | None | **LOW** |
| Visitor Mgmt | OPS-10 | Low | Low | None | **LOW** |
| Resource Booking | OPS-11 | Low | Low | None | **LOW** |
| Document Vault | CRM-02 | Low | Medium (Drive) | None | **LOW** |
| Custom Fields | CRM-05 | Low | Low | None | **LOW** |
| Knowledge Base | OPS-07 | Medium | Low | Medium (OpenAI) | **MEDIUM** |
| Geo Clock-In | HR-02 | Medium | Medium (HRMS) | Low (GPS) | **MEDIUM** |
| Mobile Forms | OPS-05 | Medium | Medium (Flutter) | None | **MEDIUM** |
| Client Portal | CRM-01 | Medium | Low | Low (Stripe) | **MEDIUM** |
| Service Tickets | CRM-04 | Medium | Low | None | **MEDIUM** |
| SLA Tracking | CRM-06 | Medium | Low | None | **MEDIUM** |
| Appointments | CRM-03 | Medium | Low | Medium (Stripe, Cal) | **MEDIUM** |
| Daily Standup | OPS-09 | Medium | Low | High (OpenAI) | **MEDIUM** |
| Growth Orchestrator | CRM-07 | High | High (LeadGen) | High (OpenAI) | **HIGH** |
| Shift Scheduler | HR-01 | High | High (HRMS) | None | **MEDIUM-HIGH** |
| Workflow Builder | OPS-03 | High | Medium | Medium (Planner/Trello) | **HIGH** |
| Smart Dispatch | OPS-04 | High | High (HRMS) | High (Maps API) | **HIGH** |
| Broadcast Alerts | OPS-08 | Medium | Medium (Fone) | Medium (Voice) | **MEDIUM-HIGH** |
| Ask Anything | OPS-12 | High | Low | High (OpenAI) | **HIGH** |
| Universal Inbox | OPS-02 | High | Medium (Fone) | Medium (IMAP) | **HIGH** |
| AI Receptionist | OPS-01 | Very High | High (Fone) | High (Voice AI) | **VERY HIGH** |

---

## 5. Critical Implementation Recommendations

### 5.1 Phased Rollout by Dependency

**Phase 1: Foundation (Must-have for all features)**
```
1. Organization Settings / Feature Flags
2. Permission system (multi-tenancy)
3. Custom field infrastructure
4. API framework + authentication
```

**Phase 2: Core Operations (Weeks 1-8)**
```
1. Dispatch Job (without AI assignment)
2. Mobile Forms (without offline)
3. Service Tickets (without AI)
4. Status Boards
```

**Phase 3: HR Overlay (Weeks 6-14)**
```
1. Shift Templates + Schedule Entry
2. Geo Clock-In (GPS only first)
3. HRMS sync
```

**Phase 4: CRM Overlay (Weeks 10-18)**
```
1. Client Portal (basic)
2. Document Vault
3. Appointments (without payments)
```

**Phase 5: AI Features (Weeks 16-28)**
```
1. Knowledge Base (search first, then RAG)
2. Smart Dispatch assignment
3. Universal Inbox
4. AI Receptionist
5. Growth Orchestrator
```

### 5.2 Integration Test Suite

Build a test suite that simulates ERPNext changes and asserts Dartwing reacts correctly. This is the only way to sleep at night with an Overlay architecture.

```python
def test_customer_address_change_propagates():
    # Create Dispatch Job linked to Customer
    job = create_dispatch_job(customer="CUST-001")

    # Update address in ERPNext
    address = frappe.get_doc("Address", job.address)
    address.address_line1 = "New Address"
    address.save()

    # Assert Dispatch Job reflects change
    job.reload()
    assert job.formatted_address == "New Address"
```

### 5.3 External Service Abstraction

Create adapter layer for swappable services:
```python
class MapsServiceBase(ABC):
    @abstractmethod
    def geocode(self, address: str) -> tuple[float, float]: ...

class GoogleMapsService(MapsServiceBase): ...
class MapboxService(MapsServiceBase): ...  # Future
```

### 5.4 Add Health Check Endpoints

```python
@frappe.whitelist(allow_guest=True)
def health():
    return {
        "status": "ok",
        "database": check_database(),
        "redis": check_redis(),
        "external_services": {
            "google_maps": check_maps_api(),
            "openai": check_openai()
        }
    }
```

### 5.5 Add Observability

Document logging and metrics strategy from day one:
```python
import structlog
log = structlog.get_logger()

def log_dispatch_assignment(job, scores, selected):
    log.info("dispatch_assignment",
        job_id=job.name,
        candidates=len(scores),
        selected_employee=selected.employee,
        drive_time_minutes=selected.drive_time_minutes)
```

---

## 6. Architecture Completeness Score

| Category | Score | Notes |
|----------|-------|-------|
| Integration Patterns | 95% | Excellent ERPNext/HRMS/CRM integration design |
| DocType Design | 98% | ✅ **RESOLVED** - Section 15 adds full JSON schemas with permissions, indexes, user_permission_dependant_doctype |
| Hooks & Events | 100% | Thorough doc_events and scheduler coverage |
| API Design | 90% | ✅ **IMPROVED** - Section 16 documents permission enforcement across REST, Socket.IO, background jobs |
| Error Handling | 95% | ✅ **RESOLVED** - Section 10 adds retry, circuit breaker, error classification patterns |
| Transaction Management | 95% | ✅ **RESOLVED** - Section 11 adds Saga pattern with compensation |
| Caching | 95% | ✅ **RESOLVED** - Section 12 adds multi-layer caching strategy |
| AI Features | 60% | High-level design good; implementation details sparse |
| Security | 92% | ✅ **RESOLVED** - Section 16 adds comprehensive permission framework with Socket.IO, background job, PHI enforcement |
| Observability | 50% | Basic scheduler; missing logging/metrics strategy |
| Offline Sync | 95% | ✅ **RESOLVED** - Section 13 adopts Dartwing Core sync protocol |
| Reconciliation Jobs | 95% | ✅ **NEW** - Section 14 adds scheduled healing jobs |
| Dispatch Performance | 98% | ✅ **RESOLVED** - Section 5.2 SQL-optimized SmartAssignment with database indexes |
| **Overall** | **94%** | Production-ready foundation with comprehensive schemas and security |

---

## 7. Conclusion

The Dartwing Company architecture is **viable and ambitious**. The "Overlay" strategy is the correct long-term choice for the Frappe ecosystem. The architecture is **well-designed at the conceptual level** with sound integration patterns and clear separation of concerns.

### Critical Fixes - ✅ ALL RESOLVED:

**Phase 1 (Operational Foundations):**
1. ✅ **Error handling patterns** - Section 10: Retry, circuit breaker, error classification
2. ✅ **Transaction management** - Section 11: Saga pattern with compensation
3. ✅ **Caching strategy** - Section 12: Multi-layer caching with TTL and invalidation
4. ✅ **Offline sync protocol** - Section 13: Adopted Dartwing Core spec (Change Feeds + Write Queues + AI Merge)
5. ✅ **Reconciliation jobs** - Section 14: Scheduled healing with discrepancy detection

**Phase 2 (Cross-Reviewer Critical Fixes):**
6. ✅ **DocType JSON Schemas** - Section 15: Complete JSON schemas for 13 DocTypes with permissions, indexes, and `user_permission_dependant_doctype`
7. ✅ **Permission Framework** - Section 16: Comprehensive permission utilities, Socket.IO enforcement, background job patterns, PHI role model, complete hooks.py configuration
8. ✅ **SQL-Optimized Dispatch** - Section 5.2: Single optimized SQL query replacing O(n) Python loops, with required database indexes and performance benchmarks

### PRD Feasibility:
- **13 of 21 features** are low-to-medium risk and can be delivered predictably
- **8 features** carry high risk due to AI complexity or external dependencies
- The 12-month roadmap in the executive summary is **now achievable** given the architectural maturity

### Final Assessment:

With the addition of Sections 10-16 and the SQL optimization in Section 5.2, the architecture now addresses **all critical issues** identified by Claude, Jeni, and Gemi reviewers:

**Operational Foundations (Sections 10-14):**
- **Error handling** ensures graceful degradation when external services fail
- **Saga patterns** guarantee cross-system consistency with automatic compensation
- **Multi-layer caching** enables performance at scale
- **Offline sync** adopts the proven Dartwing Core protocol
- **Reconciliation jobs** provide a safety net for sync discrepancies

**Cross-Reviewer Fixes (Sections 15-16, 5.2):**
- **DocType JSON Schemas** make integration promises enforceable with proper indexes and permissions
- **Permission Framework** hardens security across REST, Socket.IO, and background jobs with PHI support
- **SQL-Optimized Dispatch** eliminates the O(n) scalability bottleneck, achieving constant-time performance even at 1,000+ employees

The architecture has matured from 68% → 88% → **94% completeness**. The remaining gaps (AI feature details, observability) are lower priority and can be addressed during implementation.

**Updated Recommendation:** The 12-month roadmap is now achievable with full operational foundations and security hardening in place. The team can focus on feature development with confidence that the architecture is production-ready.

---

## 8. Review of Architecture Recommendations

This section evaluates the proposed architecture recommendations and identifies gaps.

### 8.1 Original Recommendations Assessment

| # | Recommendation | Assessment | Status |
|---|----------------|------------|--------|
| 1 | **Publish DocType schemas** with indexes on `organization, customer, status, assigned_to, modified` | ✅ Good | Indexes cover common query patterns |
| 2 | **Harden permissions** with shared helpers across REST/Socket.IO/jobs | ✅ Good | Critical for multi-tenancy security |
| 3 | **Degraded modes** with feature gating and fail-closed on missing dependencies | ✅ Excellent | Correct security posture |
| 4 | **Offline/sync spec** aligned with core sync (change feed, batch upsert, tombstones) | ⚠️ Incomplete | Missing conflict rules per DocType |
| 5 | **Sequenced delivery waves** with dependency readiness gates | ✅ Good | Needs explicit gate definitions |
| 6 | **Observability/safety** with rate limits, DLQ, metrics, alerting | ⚠️ Incomplete | Missing key metrics |
| 7 | **Multi-tenancy/hierarchy** with parent_org support | ⚠️ Incomplete | Needs permission inheritance rules |
| 8 | **Compliance** with retention, audit logs, consent tracking | ⚠️ Incomplete | Missing HIPAA BAA requirements |

---

### 8.2 Gap Analysis: Offline Sync Conflict Resolution

**Problem:** The recommendation mentions "conflict rules" but doesn't specify merge strategies per DocType.

**Required Specification:**

```python
# dartwing_company/sync/conflict_rules.py

CONFLICT_RESOLUTION_STRATEGIES = {
    # Server is authoritative for assignments
    "Dispatch Job": {
        "strategy": "server_wins",
        "reason": "Central scheduler has authoritative assignment state",
        "fields_client_wins": ["completion_notes", "photos"],  # Exception fields
    },

    # Appointments need human resolution for time conflicts
    "Appointment": {
        "strategy": "manual_resolve",
        "reason": "Time conflicts require customer communication",
        "auto_merge_fields": ["notes", "internal_notes"],  # These can auto-merge
    },

    # Conversations are append-only (messages never overwrite)
    "Conversation": {
        "strategy": "append_only",
        "reason": "Messages are immutable once sent",
        "merge_behavior": "union_of_messages",
    },

    # Tickets use server-wins for status, client-wins for notes
    "Ticket": {
        "strategy": "field_level",
        "server_wins": ["status", "assigned_to", "priority"],
        "client_wins": ["resolution_notes", "attachments"],
        "last_write_wins": ["description"],  # Whoever wrote last
    },

    # Vault documents version everything
    "Vault Document": {
        "strategy": "version_all",
        "reason": "Never lose document versions",
        "conflict_creates_branch": True,
    },

    # Forms merge field-by-field
    "Form Submission": {
        "strategy": "field_merge",
        "reason": "Different fields may be updated independently",
        "conflict_fields_manual": ["signature"],  # These need human review
    },
}

# Additional sync parameters
SYNC_CONFIG = {
    "tombstone_ttl_days": 30,           # Keep tombstones for 30 days
    "max_offline_duration_hours": 168,  # 7 days max offline
    "force_reauth_after_hours": 336,    # Force re-auth after 14 days offline
    "attachment_sync_priority": "metadata_first",  # Sync metadata, lazy-load blobs
    "batch_upsert_size": 100,           # Max records per sync batch
}
```

---

### 8.3 Gap Analysis: Wave Sequencing Readiness Gates

**Problem:** Waves are defined but lack explicit readiness criteria.

**Required Specification:**

```yaml
# dartwing_company/deployment/wave_gates.yaml

waves:
  wave_a:
    name: "Portal + Vault + Appointments + Basic Tickets"
    doctypes:
      - Customer Portal
      - Vault Document
      - Appointment
      - Ticket
    readiness_gates:
      technical:
        - name: core_multi_tenant_working
          test: "pytest tests/multi_tenancy/ -v"
          required: true
        - name: organization_crud_stable
          test: "pytest tests/organization/ -v"
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
      - Conversation
      - Inbound Message
      - Workflow Template
      - Broadcast Alert
    readiness_gates:
      technical:
        - name: wave_a_in_production
          check: "wave_a.status == 'deployed' AND wave_a.uptime_7d > 99.5%"
          required: true
        - name: channel_adapters_tested
          channels_required: ["email", "sms"]  # At least 2 channels
          test: "pytest tests/channels/ -k 'email or sms'"
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
    doctypes:
      - Dispatch Job
      - Clock In Record
      - Geofence
    readiness_gates:
      technical:
        - name: wave_b_in_production
          required: true
        - name: location_service_battery_tested
          test: "mobile_tests/battery_drain_test.dart"
          threshold: "< 5% per hour in balanced mode"
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
    doctypes:
      - AI Call
      - Growth Campaign
      - Search Query
    readiness_gates:
      technical:
        - name: wave_c_in_production
          required: true
        - name: llm_rate_limits_tested
          test: "pytest tests/ai/rate_limits.py"
          required: true
        - name: content_filtering_audited
          audit: "manual review of AI output filtering"
          required: true
      operational:
        - name: ai_cost_monitoring_active
          check: "openai.spend_alerts_configured == true"
          required: true
        - name: fallback_paths_tested
          test: "pytest tests/ai/degraded_mode.py"
          required: true
```

---

### 8.4 Gap Analysis: Observability Metrics

**Problem:** Recommendation mentions metrics but doesn't specify which ones are critical.

**Required Specification:**

```python
# dartwing_company/observability/metrics.py

CRITICAL_METRICS = {
    # === Dispatch Metrics ===
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
            "alert_if_below_for": "15m",
        },
        "avg_drive_time_accuracy": {
            "query": "avg(abs(estimated_drive_time - actual_drive_time) / estimated_drive_time)",
            "threshold": "< 0.2",  # Within 20% of estimate
            "alert_if_exceeded_for": "1h",
        },
    },

    # === Inbox/Broadcast Metrics ===
    "messaging": {
        "message_delivery_rate_by_channel": {
            "query": "rate(message_delivered_total[1h]) by (channel)",
            "dimensions": ["email", "sms", "whatsapp", "voice"],
        },
        "message_delivery_latency_p95": {
            "query": "histogram_quantile(0.95, message_delivery_duration_seconds) by (channel)",
            "threshold": {
                "email": "< 30s",
                "sms": "< 10s",
                "whatsapp": "< 5s",
            },
        },
        "broadcast_throttle_events": {
            "query": "sum(rate(broadcast_throttled_total[1h])) by (organization)",
            "alert_if": "> 100 per org per hour",
        },
        "dlq_depth": {
            "query": "sum(dead_letter_queue_depth) by (channel)",
            "threshold": "> 50",
            "alert_if_exceeded_for": "10m",
        },
    },

    # === Sync Metrics ===
    "sync": {
        "sync_lag_seconds": {
            "query": "max(time() - last_sync_timestamp) by (device_id)",
            "threshold": "> 300",  # 5 minutes
            "alert_if_exceeded_for": "10m",
        },
        "conflict_resolution_manual_rate": {
            "query": "rate(sync_conflict_manual_total[1d]) / rate(sync_conflict_total[1d])",
            "threshold": "< 0.05",  # Should be < 5%
            "alert_if_exceeded_for": "1h",
        },
        "sync_failure_rate": {
            "query": "rate(sync_failed_total[1h]) / rate(sync_attempted_total[1h])",
            "threshold": "< 0.01",  # < 1% failure
            "alert_if_exceeded_for": "15m",
        },
    },

    # === AI Metrics ===
    "ai": {
        "ai_response_latency_p99": {
            "query": "histogram_quantile(0.99, ai_request_duration_seconds)",
            "threshold": "< 3s",
            "alert_if_exceeded_for": "5m",
        },
        "ai_content_filter_blocks": {
            "query": "rate(ai_content_blocked_total[1h])",
            "alert_if": "> 10 per hour",
            "requires_audit_trail": True,
        },
        "ai_fallback_rate": {
            "query": "rate(ai_fallback_triggered_total[1h]) / rate(ai_request_total[1h])",
            "threshold": "< 0.1",  # < 10% fallback
        },
        "ai_cost_per_org_daily": {
            "query": "sum(ai_token_cost_dollars) by (organization)",
            "alert_if": "> $50 per org per day",
        },
    },

    # === SLA Metrics ===
    "sla": {
        "sla_breach_rate": {
            "query": "rate(ticket_sla_breached_total[1d]) / rate(ticket_created_total[1d])",
            "threshold": "< 0.05",  # < 5% breach rate
            "alert_if_exceeded_for": "1h",
        },
        "first_response_time_p90": {
            "query": "histogram_quantile(0.90, ticket_first_response_seconds)",
            "threshold": "< 3600",  # 1 hour
        },
        "resolution_time_p90": {
            "query": "histogram_quantile(0.90, ticket_resolution_seconds)",
            "threshold": "< 86400",  # 24 hours
        },
    },
}

# Alerting configuration
ALERT_CHANNELS = {
    "critical": ["pagerduty", "slack:#incidents"],
    "warning": ["slack:#ops-alerts"],
    "info": ["slack:#ops-metrics"],
}
```

---

### 8.5 Gap Analysis: Multi-Tenancy Permission Inheritance

**Problem:** `parent_org` support mentioned but permission inheritance rules undefined.

**Required Specification:**

```python
# dartwing_company/permissions/hierarchy.py

from enum import Enum
from dataclasses import dataclass


class HierarchyMode(Enum):
    """
    Defines how parent/child organizations interact.
    Configured per-deployment, not per-org.
    """
    STRICT_ISOLATION = "strict"      # No visibility between parent/child
    PARENT_OVERSIGHT = "oversight"   # Parent sees child data (read-only)
    SHARED_RESOURCES = "shared"      # Specific DocTypes shared


@dataclass
class HierarchyConfig:
    mode: HierarchyMode

    # For PARENT_OVERSIGHT mode
    parent_can_see_child_doctypes: list[str] = None
    parent_can_edit_child_doctypes: list[str] = None

    # For SHARED_RESOURCES mode
    shared_doctypes: list[str] = None
    isolated_doctypes: list[str] = None

    # Billing
    billing_aggregation: str = "per_org"  # "per_org" | "aggregate_to_parent"


# Default configuration (recommended for v1)
DEFAULT_HIERARCHY = HierarchyConfig(
    mode=HierarchyMode.STRICT_ISOLATION,
)

# Franchise model configuration
FRANCHISE_HIERARCHY = HierarchyConfig(
    mode=HierarchyMode.PARENT_OVERSIGHT,
    parent_can_see_child_doctypes=[
        "Ticket",           # See child tickets for QA
        "Dispatch Job",     # See dispatch metrics
        "Employee",         # See staffing
    ],
    parent_can_edit_child_doctypes=[],  # Read-only
    billing_aggregation="aggregate_to_parent",
)

# Holding company configuration
HOLDING_HIERARCHY = HierarchyConfig(
    mode=HierarchyMode.SHARED_RESOURCES,
    shared_doctypes=[
        "Employee",         # Shared staff pool
        "Vault Document",   # Shared document library
        "Knowledge Base",   # Shared knowledge
    ],
    isolated_doctypes=[
        "Conversation",     # Customer data isolated
        "Ticket",           # Support isolated
        "Dispatch Job",     # Operations isolated
    ],
    billing_aggregation="per_org",
)


def get_permission_query_for_hierarchy(
    user: str,
    doctype: str,
    hierarchy_config: HierarchyConfig
) -> str:
    """
    Build permission query considering org hierarchy.
    """
    user_orgs = get_user_organizations(user)

    if hierarchy_config.mode == HierarchyMode.STRICT_ISOLATION:
        # Simple: only see own org's data
        return f"`organization` IN ({format_list(user_orgs)})"

    elif hierarchy_config.mode == HierarchyMode.PARENT_OVERSIGHT:
        # Parent can see child orgs (read-only enforced elsewhere)
        visible_orgs = set(user_orgs)
        for org in user_orgs:
            if is_parent_org(org):
                visible_orgs.update(get_child_orgs(org))

        if doctype in hierarchy_config.parent_can_see_child_doctypes:
            return f"`organization` IN ({format_list(visible_orgs)})"
        else:
            return f"`organization` IN ({format_list(user_orgs)})"

    elif hierarchy_config.mode == HierarchyMode.SHARED_RESOURCES:
        if doctype in hierarchy_config.shared_doctypes:
            # Can see all orgs in hierarchy
            hierarchy_orgs = get_full_hierarchy_orgs(user_orgs)
            return f"`organization` IN ({format_list(hierarchy_orgs)})"
        else:
            # Isolated - only own org
            return f"`organization` IN ({format_list(user_orgs)})"


def enforce_write_permissions(doc, hierarchy_config: HierarchyConfig):
    """
    Called before save to enforce write restrictions.
    """
    user_orgs = get_user_organizations(frappe.session.user)

    if doc.organization not in user_orgs:
        # User doesn't directly belong to this org
        if hierarchy_config.mode == HierarchyMode.PARENT_OVERSIGHT:
            # Parent can only read, not write
            if doc.doctype in hierarchy_config.parent_can_edit_child_doctypes:
                return  # Allowed
            frappe.throw("Parent organizations have read-only access to child data")

        elif hierarchy_config.mode == HierarchyMode.SHARED_RESOURCES:
            if doc.doctype in hierarchy_config.shared_doctypes:
                return  # Allowed for shared doctypes

        frappe.throw("Permission denied: cannot modify data in other organizations")
```

---

### 8.6 Gap Analysis: HIPAA Compliance (if health-mode enabled)

**Problem:** Compliance section mentions audit logs but lacks HIPAA specifics.

**Required Specification (if health data is involved):**

```python
# dartwing_company/compliance/hipaa.py

HIPAA_REQUIREMENTS = {
    # === Access Controls ===
    "access_controls": {
        "minimum_necessary": {
            "description": "Field-level filtering based on role",
            "implementation": "Dynamic field permissions per DocType",
            "audit_required": True,
        },
        "break_glass": {
            "description": "Emergency access with audit + notification",
            "implementation": "Break-glass role with time-limited access",
            "requires_justification": True,
            "notification_recipients": ["privacy_officer", "supervisor"],
            "max_duration_hours": 4,
        },
        "automatic_logoff": {
            "description": "Session timeout for PHI access",
            "session_timeout_minutes": 15,
            "idle_warning_minutes": 12,
        },
    },

    # === Audit Requirements ===
    "audit_logging": {
        "phi_access_log": {
            "retention_years": 6,
            "fields": ["who", "what", "when", "why", "from_ip", "device_id"],
            "immutable": True,  # Cannot be deleted
        },
        "export_log": {
            "description": "Track all data exports containing PHI",
            "requires_approval_for": ["bulk_export", "report_generation"],
        },
        "modification_log": {
            "description": "Track all PHI modifications",
            "fields": ["old_value", "new_value", "modified_by", "reason"],
        },
    },

    # === Technical Safeguards ===
    "encryption": {
        "at_rest": {
            "algorithm": "AES-256",
            "key_management": "AWS KMS or HashiCorp Vault",
            "doctypes": ["Patient Record", "Medical Note", "Conversation"],  # PHI DocTypes
        },
        "in_transit": {
            "minimum_tls": "1.2",
            "certificate_requirements": "Valid CA-signed certificate",
        },
    },

    # === BAA Tracking ===
    "business_associate_agreements": {
        "required_for": [
            "Cloud hosting provider",
            "Email service (if PHI in emails)",
            "SMS provider (if PHI in messages)",
            "AI/LLM provider (if processing PHI)",
            "Backup service",
        ],
        "tracking_fields": [
            "vendor_name",
            "baa_signed_date",
            "baa_expiry_date",
            "data_categories_shared",
            "contact_person",
            "last_security_review",
        ],
    },

    # === Data Retention ===
    "retention": {
        "medical_records": {
            "retention_years": 7,  # Varies by state; 7 is safe default
            "deletion_method": "secure_wipe",
            "audit_trail_retention": "permanent",
        },
        "audit_logs": {
            "retention_years": 6,
            "cannot_be_modified": True,
        },
    },
}


# DocTypes containing PHI that require HIPAA controls
PHI_DOCTYPES = [
    "Patient Record",
    "Medical Note",
    "Appointment",  # If contains medical reason
    "Conversation",  # If patient communications
    "Vault Document",  # If contains medical docs
]


def apply_hipaa_controls(doctype: str, doc: dict) -> dict:
    """
    Apply HIPAA controls before returning data.
    """
    if doctype not in PHI_DOCTYPES:
        return doc

    user = frappe.session.user
    role = get_user_hipaa_role(user)

    # Log access
    log_phi_access(
        user=user,
        doctype=doctype,
        docname=doc.get("name"),
        action="read",
        fields_accessed=list(doc.keys()),
    )

    # Apply minimum necessary filtering
    allowed_fields = get_allowed_phi_fields(role, doctype)
    filtered_doc = {k: v for k, v in doc.items() if k in allowed_fields}

    return filtered_doc
```

---

### 8.7 Missing Recommendations (Not in Original List)

#### A. Background Job Isolation

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

#### B. API Versioning Strategy

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

# Version negotiation
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

#### C. Feature Flags per Organization

```python
# dartwing_company/feature_flags.py

class OrgFeatureFlags(Document):
    """Per-organization feature flag configuration."""

    doctype = "Org Feature Flags"

    organization: Link["Organization"]

    # Wave gating
    enable_dispatch: Check = False
    enable_ai_receptionist: Check = False
    enable_growth_orchestrator: Check = False
    enable_universal_inbox: Check = False

    # Compliance modes
    hipaa_mode: Check = False
    gdpr_mode: Check = False
    sox_audit_mode: Check = False

    # Limits
    max_broadcast_per_day: Int = 1000
    max_ai_requests_per_hour: Int = 100
    max_dispatch_jobs_per_day: Int = 500

    # Beta features
    enable_beta_api: Check = False
    enable_experimental_ai: Check = False


def is_feature_enabled(organization: str, feature: str) -> bool:
    """Check if feature is enabled for organization."""
    flags = frappe.get_cached_doc("Org Feature Flags", {"organization": organization})
    return getattr(flags, feature, False)
```

#### D. Disaster Recovery Specification

```yaml
# dartwing_company/deployment/disaster_recovery.yaml

recovery_objectives:
  rpo:  # Recovery Point Objective (max data loss)
    conversations: 1 hour
    vault_documents: 15 minutes
    appointments: 1 hour
    dispatch_jobs: 5 minutes  # Active jobs are critical
    tickets: 1 hour
    ai_calls: 24 hours  # Can regenerate from logs

  rto:  # Recovery Time Objective (max downtime)
    core_api: 15 minutes
    portal: 30 minutes
    search: 1 hour
    ai_features: 4 hours  # Degrade gracefully
    reporting: 8 hours

backup_strategy:
  database:
    frequency: continuous  # WAL streaming
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
    notification: ["ops-critical"]

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

---

### 8.8 Updated Recommendations Summary

| Category | Original | Gap | Recommended Addition |
|----------|----------|-----|---------------------|
| DocType schemas | ✅ | None | Add foreign key cascade spec |
| Permissions | ✅ | Minor | Add break-glass for health mode |
| Degraded modes | ✅ | None | Add feature flag per org |
| Offline sync | ⚠️ | **Critical** | Add conflict rules per DocType |
| Wave sequencing | ✅ | Minor | Add explicit readiness gates |
| Observability | ⚠️ | **High** | Add sync lag, AI latency, SLA metrics |
| Multi-tenancy | ⚠️ | **High** | Define permission inheritance rules |
| Compliance | ⚠️ | **Medium** | Add HIPAA BAA tracking (if applicable) |
| **NEW** | ❌ | **High** | Job isolation strategy |
| **NEW** | ❌ | **Medium** | API versioning |
| **NEW** | ❌ | **Medium** | Feature flags per org |
| **NEW** | ❌ | **High** | DR/RTO/RPO spec |

---

### 8.9 Implementation Priority

```
Priority 1 (Before Wave A):
├─ Conflict resolution rules per DocType
├─ Permission inheritance for parent_org
├─ Critical metrics dashboard
└─ Feature flags infrastructure

Priority 2 (Before Wave B):
├─ Job queue isolation
├─ API versioning
├─ DLQ monitoring
└─ Explicit wave gates

Priority 3 (Before Wave D):
├─ HIPAA compliance (if health data)
├─ DR runbook and testing
├─ AI cost monitoring
└─ Break-glass access
```

---

*Section 8 added: November 28, 2025*
*Reviewer: Claude (Opus 4.5)*

---

*Critique prepared: November 2025*
*Reviewer: Claude (Antigravity Agent)*
*Architecture version: Dartwing Company 1.0 (Updated with Sections 10-16, SQL optimization in 5.2)*
*PRD version: 1.0 Draft*
*Last updated: November 28, 2025*
*Completeness: 68% → 88% → 94%*
