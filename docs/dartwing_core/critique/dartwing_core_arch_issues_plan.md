# Plan: Implement Dartwing Core Architecture Issues

## Objective
Create/update documentation files to address the 5 still-valid architecture issues from the critique.

## Approach
- **Separate spec files** (Option A) following existing naming pattern (`*_spec.md`)

## Issues to Address

| Priority | Issue | Action |
|----------|-------|--------|
| 🔴 P0 | Socket.IO Redis adapter | Create new spec |
| 🔴 P0 | Integration token manager | Create new spec |
| 🟠 P1 | Per-DocType conflict rules | Update existing sync spec |
| 🟠 P1 | Full-stack observability | Create new spec |
| 🟠 P1 | Background job isolation | Create new spec |

## Implementation Plan

### 1. Create `socket_io_scaling_spec.md` (P0)
**Path:** `/docs/dartwing_core/socket_io_scaling_spec.md`

**Contents:**
- Objective & goals
- Redis adapter architecture (pub/sub pattern)
- Python-side implementation (patch `frappe.publish_realtime`)
- Node.js Socket.IO configuration with `@socket.io/redis-adapter`
- Nginx sticky sessions configuration
- Room management across nodes
- Observability (connection counts, message rates)
- Test matrix

**Reference:** Use `offline_real_time_sync_spec.md` as template

---

### 2. Create `integration_token_management_spec.md` (P0)
**Path:** `/docs/dartwing_core/integration_token_management_spec.md`

**Contents:**
- Objective & goals
- Token lifecycle (OAuth2 refresh flow)
- `TokenManager` class architecture
- Encryption strategy (Fernet/AES-256)
- Proactive refresh scheduler (cron job)
- Thread-safe locking pattern
- Admin notification on expiry
- Credential storage (frappe.conf vs Vault)
- Test matrix

**Reference:** Use `dartwing_auth_arch.md` as template

---

### 3. Update `offline_real_time_sync_spec.md` (P1)
**Path:** `/docs/dartwing_core/offline_real_time_sync_spec.md`

**Add Section:** Per-DocType Conflict Resolution Rules

**Contents to Add:**
```markdown
## Per-DocType Conflict Strategies

| DocType | Strategy | Server Wins | Client Wins | Notes |
|---------|----------|-------------|-------------|-------|
| Organization | server_wins | all | - | Authoritative |
| Person | server_wins | all | - | Identity data |
| Task | field_level | status, assigned_to | notes | Collaborative |
| Calendar Event | manual_resolve | - | - | Time conflicts |
| Notification | client_wins | - | read_state | User-local |
| Comment | append_only | - | - | Union merge |
| _default | server_wins | all | - | Fallback |
```

---

### 4. Create `observability_spec.md` (P1)
**Path:** `/docs/dartwing_core/observability_spec.md`

**Contents:**
- Objective & goals
- Metric categories (HTTP, background jobs, database, integrations)
- Prometheus-style metric definitions
- Structured logging format (JSON)
- Log aggregation strategy
- Alert thresholds and channels
- Dashboard requirements
- Integration with existing sync observability

**Reference:** Extend metrics from `offline_real_time_sync_spec.md`

---

### 5. Create `background_job_isolation_spec.md` (P1)
**Path:** `/docs/dartwing_core/background_job_isolation_spec.md`

**Contents:**
- Objective & goals
- Queue strategy (critical, default, bulk)
- Per-org job limits to prevent noisy neighbor
- Worker allocation per queue
- Dead letter queue (DLQ) configuration
- Retry strategy with exponential backoff
- Job monitoring and stuck job detection
- Permission enforcement in async context
- Test matrix

**Reference:** Use `org_integrity_guardrails.md` as template

---

### 6. Update `dartwing_core_arch.md` with Cross-References

**Add cross-references in these sections:**
- Section 2.2 (API Gateway) → link to `socket_io_scaling_spec.md`
- Section 5 (Authentication) → link to `integration_token_management_spec.md`
- Section 10 (Technical Specs) → link to `observability_spec.md`
- Section 11 (Advanced Features) → link to `background_job_isolation_spec.md`

---

### 7. Update `dartwing_core_arch_issues.md` Status

Mark issues as **RESOLVED** with links to new specs:
- Update Part 2 sections with "✅ Resolved" status
- Add links to new specification documents
- Update Architecture Completeness Score

---

## File Creation Order

1. `socket_io_scaling_spec.md` (P0 - blocker for real-time)
2. `integration_token_management_spec.md` (P0 - blocker for integrations)
3. Update `offline_real_time_sync_spec.md` (P1 - quick addition)
4. `background_job_isolation_spec.md` (P1)
5. `observability_spec.md` (P1)
6. Update `dartwing_core_arch.md` cross-references
7. Update `dartwing_core_arch_issues.md` status

## Estimated Effort
- 4 new spec documents: ~2-3 hours each
- 3 document updates: ~30 min each
- **Total: ~10-12 hours**

## Critical Files to Read Before Implementation
- `/docs/dartwing_core/offline_real_time_sync_spec.md` (template + update target)
- `/docs/dartwing_core/dartwing_auth_arch.md` (template for token spec)
- `/docs/dartwing_core/org_integrity_guardrails.md` (template for job spec)
- `/docs/dartwing_core/dartwing_core_arch.md` (update target)

---

_Plan created: November 2025_
