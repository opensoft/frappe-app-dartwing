# Offline Sync Problem Statement

**Module:** dartwing_company
**Status:** Critical Gap
**Date:** December 2025

---

## 1. Executive Summary

Offline synchronization is one of the hardest problems in distributed systems. The fundamental challenge is maintaining data consistency when multiple devices can modify the same data while disconnected from the server.

**The CAP theorem** tells us we cannot have all three of:
- **Consistency** (all nodes see the same data)
- **Availability** (every request receives a response)
- **Partition tolerance** (system continues despite network failures)

Mobile-first applications like Dartwing must choose **Availability + Partition Tolerance**, which means we accept **eventual consistency** and must have explicit strategies to handle conflicts when they occur.

---

## 2. The Overlay Architecture Challenge

Dartwing Company's position in the architecture creates unique sync complexity:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUTTER MOBILE APP                            │
│                    (Offline-capable)                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                    [Sync Layer]
                          │
┌─────────────────────────┴───────────────────────────────────────┐
│                    DARTWING COMPANY                              │
│   Dispatch Job │ Appointment │ Conversation │ Ticket │ Forms    │
│                                                                  │
│   Uses: dartwing_core sync protocol                              │
│   Problem: No conflict rules defined for Company DocTypes        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────────────┐
│                    DARTWING CORE                                 │
│   Organization │ Person │ Task │ Notification                    │
│                                                                  │
│   ✓ Has: offline_real_time_sync_spec.md                          │
│   ✓ Has: CONFLICT_STRATEGIES for core DocTypes                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────────────┐
│                    FRAPPE ECOSYSTEM                              │
│   ERPNext │ HRMS │ CRM │ Health │ Drive                          │
│                                                                  │
│   ⚠️ External: Cannot modify sync behavior                       │
│   ⚠️ Risk: Direct SQL updates bypass hooks                       │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Is Complicated

1. **Company DocTypes link to Frappe DocTypes**: A `Dispatch Job` links to an ERPNext `Customer` and `Address`. If the address changes while the tech is offline, the job has stale location data.

2. **Multiple users edit the same records**: An office manager and field tech might both update a `Ticket` while one is offline.

3. **Time-sensitive operations**: `Appointments` have time slots that can conflict. `Dispatch Jobs` have assignment states that must be authoritative.

4. **Child table complexity**: A `Conversation` has many `Messages`. New messages from multiple offline devices must merge correctly.

5. **Cross-module dependencies**: Completing a `Dispatch Job` creates an ERPNext `Sales Invoice` and HRMS `Timesheet`. These cross-system transactions cannot be partially applied.

---

## 3. Problem Scenarios

### Scenario 1: Dispatch Job Reassignment

```
Timeline:
─────────────────────────────────────────────────────────────────►
     │                    │                    │
     │                    │                    │
Tech A receives       Office reassigns      Tech A comes
job JOB-001           JOB-001 to Tech B     back online
(goes offline)        (Tech A doesn't know)
     │                    │                    │
     ▼                    ▼                    ▼
Local state:          Server state:         CONFLICT!
JOB-001               JOB-001               Tech A's app shows
assigned: Tech A      assigned: Tech B      JOB-001 but they
status: In Progress   status: Unassigned    shouldn't have it
```

**Problem:** Tech A drove to the job site not knowing it was reassigned. Wasted time, confused customer, two techs might arrive.

**Risk Level:** HIGH - Operational chaos, customer complaints

---

### Scenario 2: Appointment Double-Booking

```
Timeline:
─────────────────────────────────────────────────────────────────►
     │                    │                    │
     │                    │                    │
Receptionist A        Receptionist B        Both sync
books 2pm slot        books same 2pm slot   to server
for Client X          for Client Y
(offline)             (offline)
     │                    │                    │
     ▼                    ▼                    ▼
Local state:          Local state:          CONFLICT!
APT-001               APT-002               Two appointments
2pm: Client X         2pm: Client Y         for same slot
```

**Problem:** Two clients arrive at the same time expecting their appointment.

**Risk Level:** HIGH - Customer experience disaster

---

### Scenario 3: Conversation Message Ordering

```
Timeline:
─────────────────────────────────────────────────────────────────►
     │                    │                    │
     │                    │                    │
Support Agent         Customer sends        Agent syncs,
sends "We'll fix      "Never mind, I        sees customer
it tomorrow"          fixed it myself"      already resolved
(offline)             (via web)
     │                    │                    │
     ▼                    ▼                    ▼
Local state:          Server state:         MERGE NEEDED
Conv has msg:         Conv has msg:         Final conversation
"We'll fix..."        "Never mind..."       should have BOTH
                                            messages in order
```

**Problem:** Messages aren't lost, but ordering matters. Customer shouldn't get "We'll fix it tomorrow" after they said they fixed it.

**Risk Level:** MEDIUM - Confusing but not data loss

---

### Scenario 4: Ticket Status Race Condition

```
Timeline:
─────────────────────────────────────────────────────────────────►
     │                    │                    │
     │                    │                    │
Tech marks ticket     Manager escalates     Both sync
as "Resolved"         ticket to "Urgent"    simultaneously
(offline)             (online)
     │                    │                    │
     ▼                    ▼                    ▼
Local state:          Server state:         CONFLICT!
TKT-001               TKT-001               Which status wins?
status: Resolved      status: Urgent        Resolved? Urgent?
                      priority: High        SLA implications!
```

**Problem:** If "Resolved" wins, an urgent issue is ignored. If "Urgent" wins, resolved work is redone.

**Risk Level:** HIGH - SLA breach risk

---

### Scenario 5: Form Submission with Signature

```
Timeline:
─────────────────────────────────────────────────────────────────►
     │                    │                    │
     │                    │                    │
Tech fills form       Office updates        Tech syncs
with customer         form template         with signature
signature             (adds required field) (missing new field)
(offline)
     │                    │                    │
     ▼                    ▼                    ▼
Local state:          Server state:         CONFLICT!
Form complete         Template changed      Is form valid?
with signature        new field required    Signature is on
                                            old version
```

**Problem:** Legally binding signature was captured on an outdated form version.

**Risk Level:** HIGH - Compliance/legal risk

---

### Scenario 6: Geo Clock-In Validation

```
Timeline:
─────────────────────────────────────────────────────────────────►
     │                    │                    │
     │                    │                    │
Employee clocks       Geofence boundary     Employee syncs
in at Job Site A      is updated to         clock-in record
(offline, GPS ok)     exclude that area
     │                    │                    │
     ▼                    ▼                    ▼
Local state:          Server state:         CONFLICT!
Clock-in valid        Geofence changed      Was clock-in
at recorded GPS       Area no longer valid  legitimate?
```

**Problem:** Clock-in was valid at the time but appears invalid after sync.

**Risk Level:** MEDIUM - Payroll disputes

---

## 4. Current State Analysis

### What dartwing_core Provides

The core module has a well-defined sync specification in `offline_real_time_sync_spec.md`:

| Component | Status | Description |
|-----------|--------|-------------|
| Change Feed API | ✅ Defined | `/api/method/dartwing_core.sync.feed` |
| Write Queue API | ✅ Defined | `/api/method/dartwing_core.sync.upsert_batch` |
| Socket.IO Channels | ✅ Defined | Real-time delta streaming |
| Conflict Strategies | ✅ Defined | 6 strategy types available |
| Core DocType Rules | ✅ Defined | Organization, Person, Task, etc. |

### What dartwing_company Is Missing

| Component | Status | Gap |
|-----------|--------|-----|
| Conflict rules for Dispatch Job | ❌ Missing | No strategy defined |
| Conflict rules for Appointment | ❌ Missing | No strategy defined |
| Conflict rules for Conversation | ❌ Missing | No strategy defined |
| Conflict rules for Ticket | ❌ Missing | No strategy defined |
| Conflict rules for Vault Document | ❌ Missing | No strategy defined |
| Conflict rules for Form Submission | ❌ Missing | No strategy defined |
| Conflict rules for Clock In Record | ❌ Missing | No strategy defined |
| Conflict rules for Schedule Entry | ❌ Missing | No strategy defined |
| Conflict rules for Workflow Instance | ❌ Missing | No strategy defined |
| Conflict rules for Broadcast Alert | ❌ Missing | No strategy defined |
| Conflict rules for Growth Campaign | ❌ Missing | No strategy defined |
| Conflict rules for AI Call | ❌ Missing | No strategy defined |
| Child table merge logic | ❌ Missing | Messages, line items |
| Cross-module transaction handling | ❌ Missing | ERPNext/HRMS creates |

---

## 5. Risk Assessment

### If Not Addressed

| Risk | Likelihood | Impact | Consequence |
|------|------------|--------|-------------|
| Data loss | High | Critical | Customer signatures lost, work records missing |
| Double-booking | High | High | Two customers for same slot, reputation damage |
| Wrong assignments | High | High | Techs go to wrong jobs, wasted time and fuel |
| SLA breaches | Medium | High | Tickets resolved incorrectly, penalties |
| Payroll disputes | Medium | Medium | Clock-in records contested |
| Compliance violations | Low | Critical | Invalid forms with signatures, legal liability |
| Split-brain state | High | Critical | Server and client permanently diverge |

### Business Impact

1. **Field Operations:** Technicians cannot trust their mobile app data
2. **Customer Experience:** Appointments and communications become unreliable
3. **Compliance:** Form signatures may be invalid
4. **Support Burden:** Manual reconciliation of conflicts
5. **Trust:** Users lose confidence in the platform

---

## 6. DocTypes Requiring Conflict Resolution Rules

### Priority 1: Mission-Critical (Must have before Wave C)

| DocType | Primary Challenge | Recommended Strategy |
|---------|-------------------|---------------------|
| **Dispatch Job** | Assignment state must be authoritative | `server_wins` with client field exceptions |
| **Appointment** | Time slot conflicts | `manual_resolve` |
| **Clock In Record** | GPS validation timing | `server_wins` |

### Priority 2: High-Value (Must have before Wave B)

| DocType | Primary Challenge | Recommended Strategy |
|---------|-------------------|---------------------|
| **Conversation** | Message ordering | `append_only` for messages |
| **Inbound Message** | Never lose messages | `append_only` |
| **Ticket** | Status vs notes conflict | `field_level` |
| **Vault Document** | Never lose versions | `version_all` |

### Priority 3: Important (Must have before Wave A)

| DocType | Primary Challenge | Recommended Strategy |
|---------|-------------------|---------------------|
| **Form Submission** | Signature validity | `field_level` with manual for signature |
| **Form Template** | Version compatibility | `server_wins` |
| **Schedule Entry** | Shift conflicts | `server_wins` |
| **Shift Template** | Template authority | `server_wins` |

### Priority 4: Lower Risk (Can defer to Wave D)

| DocType | Primary Challenge | Recommended Strategy |
|---------|-------------------|---------------------|
| **Workflow Instance** | State machine integrity | `server_wins` |
| **Broadcast Alert** | Delivery tracking | `server_wins` |
| **Growth Campaign** | Campaign state | `server_wins` |
| **AI Call** | Transcript append | `append_only` |

---

## 7. Conclusion

The offline sync problem for dartwing_company is **critical** and **unresolved**. The core sync protocol provides the infrastructure, but Company-specific conflict resolution rules are completely undefined.

Without these rules:
- The mobile app will exhibit undefined behavior during conflicts
- Data loss is likely during normal operations
- Users will lose trust in the platform
- The "offline-first" promise cannot be delivered

**Next Step:** See `sync_resolution_plan.md` for the complete solution architecture.

---

*Document created: December 2025*
*Related: [dartwing_core/offline_real_time_sync_spec.md](../../dartwing_core/offline_real_time_sync_spec.md)*
