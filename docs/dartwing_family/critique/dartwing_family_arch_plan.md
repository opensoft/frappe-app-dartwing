# Dartwing Family Architecture Implementation Plan

**Source:** Synthesized from `dartwing_family_arch_issues.md` (13 issues across Critical/High/Medium severity)
**Current State:** Module is 8-12% implemented with significant gaps
**Goal:** Address all documented issues through phased implementation

---

## Executive Summary

The Dartwing Family module has foundational code (2 basic DocTypes, CRUD APIs) but is missing critical infrastructure (permissions, org-scoping, sync, compliance). This plan prioritizes:
1. **Technical debt cleanup** (conflicting APIs, missing hooks)
2. **Core infrastructure** (Organization model, permissions, age-based access)
3. **Essential features** (relationships, custody, chores)
4. **Advanced features** (integrations, location, gamification)

---

## Phase 1: Foundation & Cleanup (Weeks 1-4)

### 1.1 API Consolidation (Days 1-2)
**Addresses:** Conflicting API implementations

| Task | File | Action |
|------|------|--------|
| Delete outdated API | `/dartwing/api/family.py` | DELETE |
| Keep correct implementation | `/dartwing/api/v1.py` | KEEP (uses correct field names) |
| Update documentation | `/API.md`, `/STRUCTURE.md` | MODIFY |

### 1.2 Organization Model (Days 3-7)
**Addresses:** M2 (Multi-tenant depth), Architecture foundation

**Create Organization DocType:**
```
/dartwing/dartwing_core/doctype/organization/
├── organization.json
├── organization.py
└── __init__.py
```

**Fields:**
- `org_name` (Data, required)
- `org_type` (Select: Family/Company/Club/Nonprofit, set_only_once)
- `linked_doctype`, `linked_name` (read_only, auto-set)
- `status` (Active/Inactive/Dissolved)

**Modify Family DocType:**
- Add `organization` Link field (required, read_only)
- Add `user_permission_dependant_doctype: "Organization"` to JSON

### 1.3 Permission Infrastructure (Days 8-12)
**Addresses:** H1 (Permission enforcement thin)

**Create permission module:**
```
/dartwing/permissions/
├── __init__.py
└── family.py
```

**Configure hooks.py:**
```python
permission_query_conditions = {
    "Family": "dartwing.permissions.family.get_permission_query_conditions",
    "Family Member": "dartwing.permissions.family.get_member_permission_query_conditions",
}

has_permission = {
    "Family": "dartwing.permissions.family.has_permission",
}

fixtures = [
    {"doctype": "Role", "filters": [["name", "in", [
        "Family Manager", "Family Admin", "Family Parent",
        "Family Teen", "Family Child", "Family Extended"
    ]]]}
]
```

### 1.4 Family Member Enhancement (Days 13-15)
**Addresses:** M3 (DocType proliferation), H4 (Compliance gaps)

**Approach:** Keep as child table (hybrid architecture), enhance with age fields

**Add fields to existing Family Member child table:**
- `first_name`, `last_name` (split from full_name)
- `date_of_birth` (Date, required for minors)
- `user_account` (Link to User, optional)
- `age` (Int, computed in controller)
- `age_category` (Data, computed: Toddler/Child/Teen/Adult)
- `is_minor`, `is_coppa_protected` (Check, computed)

**Update controller:**
```python
# family_member.py
def validate(self):
    if self.date_of_birth:
        self.age = calculate_age(self.date_of_birth)
        self.age_category = get_age_category(self.age)
        self.is_minor = self.age < 18
        self.is_coppa_protected = self.age < 13
```

**No migration needed** - enhancing existing child table in place

### 1.5 Test Infrastructure (Days 16-20)
**Addresses:** Quality assurance, regression prevention

**Create tests:**
```
/dartwing/dartwing_core/doctype/family/test_family.py
/dartwing/dartwing_core/doctype/organization/test_organization.py
/dartwing/tests/test_api_v1.py
/dartwing/tests/test_family_permissions.py
```

**Minimum coverage:**
- Family CRUD operations
- Organization-Family linking
- Permission isolation (user sees only own org)
- Age calculation accuracy

---

## Phase 2: Core Family Features (Weeks 5-8)

### 2.1 Family Relationship Modeling (Week 5)
**Addresses:** M4 (Custody edge cases), Complex family structures

**Create Family Relationship DocType:**
- `from_member`, `to_member` (Links to Family Member)
- `relationship_type` (Parent/Child/Spouse/Sibling/Grandparent/Other)
- `organization` (for scoping)

**Implement bidirectional auto-creation:**
- Parent→Child creates Child→Parent
- Spouse→Spouse creates reciprocal

### 2.2 Age-Based Permission System (Week 6)
**Addresses:** H4 (COPPA compliance), Feature gating

**Create age utilities:**
```
/dartwing/dartwing_family/age_utils.py
```

**Age categories:**
| Category | Age Range | COPPA Status | Access Level |
|----------|-----------|--------------|--------------|
| Toddler | 0-5 | N/A | Parent-managed only |
| Child | 6-12 | Protected | Kid-mode, limited |
| Teen | 13-17 | Not protected | Parental controls |
| Adult | 18+ | N/A | Full autonomy |

**Scheduler for age transitions:**
```python
# hooks.py
scheduler_events = {
    "daily": ["dartwing_family.tasks.daily_age_check"]
}
```

### 2.3 Basic Custody Schedule (Week 7)
**Addresses:** H5 (Operational safety), M4 (Custody edge cases)

**Create Custody Schedule DocType:**
- `child` (Link to Family Member)
- `schedule_type` (50/50 Weekly, Bi-Weekly, Primary/Visitation, Custom)
- `parent_a`, `parent_b` (Links)
- `effective_date`, `schedule_data` (JSON for custom)

**API endpoints:**
- `get_custody_for_date(child, date)`
- `get_custody_calendar(child, start_date, end_date)`

**Deferred:** Holiday overrides, timezone handling → Phase 4

### 2.4 Emergency Contacts (Week 8)
**Addresses:** Safety-critical feature

**Create Emergency Contact DocType:**
- `family_member` (Link)
- `contact_name`, `phone`, `email`
- `relationship`, `is_authorized_pickup`
- `priority` (1=primary)

---

## Phase 3: Real-Time & Offline (Weeks 9-12)

### 3.1 Socket.IO Room Pattern (Week 9)
**Addresses:** H2 (Sync undefined), Real-time updates

**Channel pattern:** `family_{organization_id}`

**Implementation:**
```python
# /dartwing/dartwing_family/realtime.py
frappe.publish_realtime(
    "family_event",
    {"type": "member_updated", "data": {...}},
    room=f"family_{org_id}",
    after_commit=True
)
```

**Doc event hooks for broadcasting:**
```python
# hooks.py
doc_events = {
    "Family Member": {"on_update": "dartwing_family.realtime.broadcast_member_event"},
    "Chore Assignment": {"on_update": "dartwing_family.realtime.broadcast_chore_event"},
}
```

### 3.2 Offline Sync Specification (Weeks 10-11)
**Addresses:** H2 (Offline/sync undefined)

**Offline-available data:**
- Emergency contacts (always cached)
- Family member basic info
- Active chore assignments
- Custody schedule

**Online-only operations:**
- Financial transactions
- Location updates
- Medical record modifications

**Create sync endpoints:**
- `/api/method/dartwing_core.sync.feed` - Change feed with pagination
- `/api/method/dartwing_core.sync.upsert_batch` - Batch write with conflict detection

**Conflict resolution strategy:**
- Last-Write-Wins for simple fields (with Version history)
- Server-wins for financial data
- Manual resolution only for critical conflicts

### 3.3 Chore System (Week 12)
**Addresses:** Core family feature

**Create Chore Template DocType:**
- `title`, `description`, `estimated_minutes`
- `organization` (scoping)
- `age_appropriate_min`, `age_appropriate_max`

**Create Chore Assignment DocType:**
- `template` (Link), `assigned_to` (Link to Family Member)
- `due_date`, `status` (Pending/In Progress/Completed/Verified)
- `completed_at`, `verified_by`

**Deferred:** Points, streaks, rewards → Phase 4

---

## Phase 4: Advanced Features (Weeks 13-20)

### 4.1 Integration Adapter Framework (Weeks 13-14)
**Addresses:** C2 (Integration fragility)

**Create abstract adapter pattern:**
```python
class IntegrationAdapter(ABC):
    def authenticate(self) -> bool
    def sync_data(self) -> SyncResult
    def health_check(self) -> HealthStatus
```

**First integration:** Google Calendar (reference implementation)

### 4.2 Location Features (Weeks 15-16)
**Addresses:** H3 (Location privacy)

**Implement check-in model (NOT real-time tracking):**
- Single current location per member
- Privacy controls (who can see)
- Automatic data expiry (7 days teens, 24 hours adults default)

### 4.3 Gamification with Guardrails (Weeks 17-18)
**Addresses:** M5 (Gamification balance)

**Add to chores:**
- Point values per chore
- Daily/weekly point caps (max 100/day)
- Parent override controls

### 4.4 Compliance Infrastructure (Weeks 19-20)
**Addresses:** H4 (Compliance details missing)

**Create Consent Log DocType:**
- `person`, `consent_type`, `consent_given`
- `consent_date`, `consenting_user`
- `withdrawal_date`

**Create retention policies:**
- Location: 7 days (teens), 24 hours (adults)
- Change logs: 30 days
- Audit trails: 3-7 years

---

## Deferred Features (Post-MVP)

Per the issues document recommendations, explicitly defer:
- Voice Cloning/AI Assistant (C3) - Legal complexity
- Real-time Location Tracking - Start with check-in only
- Camera-based Recognition - Requires ML infrastructure
- Vehicle Telematics - Hardware complexity
- Advanced Home Automation - 5+ platform integrations
- Education Platform Sync - 8+ OAuth integrations
- Weather Automation - Not core to family management

---

## Critical Files to Modify/Create

### Files to DELETE
- `/dartwing/api/family.py` - Conflicting API with wrong field names

### Files to CREATE
| File | Purpose |
|------|---------|
| `/dartwing/dartwing_core/doctype/organization/` | Organization thin shell |
| `/dartwing/permissions/family.py` | Permission query conditions |
| `/dartwing/dartwing_family/age_utils.py` | Age calculation and COPPA checks |
| `/dartwing/dartwing_family/realtime.py` | Socket.IO room management |
| `/dartwing/dartwing_core/sync.py` | Change feed and batch upsert |

### Files to MODIFY
| File | Changes |
|------|---------|
| `/dartwing/hooks.py` | Add permission_query_conditions, fixtures, scheduler_events, doc_events |
| `/dartwing/dartwing_core/doctype/family/family.json` | Add organization link field |
| `/dartwing/dartwing_core/doctype/family/family.py` | Add organization validation |
| `/dartwing/dartwing_core/doctype/family_member/family_member.json` | Add age fields (keep as child table) |
| `/dartwing/dartwing_core/doctype/family_member/family_member.py` | Add age calculation in validate() |
| `/fixtures/role.json` | Add all family roles |

---

## Success Criteria by Phase

### Phase 1 Complete When:
- [ ] Single API file with correct field names
- [ ] Organization model with Family linking
- [ ] Permission isolation working (user sees only own org)
- [ ] Age calculation accurate
- [ ] All tests passing

### Phase 2 Complete When:
- [ ] Bidirectional relationships working
- [ ] COPPA flags enforced at API level
- [ ] Basic custody schedule functional
- [ ] Emergency contacts accessible

### Phase 3 Complete When:
- [ ] Real-time updates broadcasting to family rooms
- [ ] Offline sync spec documented and endpoints working
- [ ] Chore assignment/completion flow working

### Phase 4 Complete When:
- [ ] One integration (Google Calendar) working
- [ ] Check-in location with privacy controls
- [ ] Point system with guardrails
- [ ] Consent logging and retention enforced

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| Phase 1 | 4 weeks | Stable foundation, proper architecture |
| Phase 2 | 4 weeks | Core family features, COPPA compliance |
| Phase 3 | 4 weeks | Real-time updates, offline spec, chores |
| Phase 4 | 8 weeks | Integrations, location, gamification |

**Total MVP (Phases 1-3):** 12 weeks
**Full Feature Set:** 20 weeks
