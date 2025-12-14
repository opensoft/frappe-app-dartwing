# MASTER ACTION PLAN: 007-Equipment-DocType

**Synthesized By:** Director of Engineering
**Date:** 2025-12-14
**Branch:** `007-equipment-doctype`
**Reviews Consolidated:** opus45, geni30, grokf1, jeni52, sonn45

---

## 1. Master Action Plan (Prioritized & Consolidated)

| Priority | Type | Source(s) | Issue Description (Consolidated) | Actionable Fix |
|:---------|:-----|:----------|:---------------------------------|:---------------|
| **P1-01** | Security | jeni52, sonn45 | **SQL Injection via Double-Quoting in Permission Query.** `frappe.db.escape()` already returns quoted strings; wrapping in additional quotes (`f"'{frappe.db.escape(o)}'"`) breaks the escape mechanism and creates SQL injection vulnerability. This will cause Equipment list queries to fail or be exploitable. | In `dartwing/permissions/equipment.py:46`, change `org_list = ", ".join(f"'{frappe.db.escape(o)}'" for o in orgs)` to `org_list = ", ".join(frappe.db.escape(o) for o in orgs)`. Reference the corrected pattern in `dartwing/permissions/company.py:34`. |
| **P1-02** | Security | jeni52, sonn45 | **Cross-Tenant Data Leak in `get_org_members()`.** The whitelisted method accepts any `organization` parameter without verifying the caller has User Permission for that organization. Attackers can enumerate Person records from organizations they shouldn't access, violating tenant isolation (FR-003/FR-009). | Before the SQL query in `equipment.py:140`, add authorization check: `if not frappe.has_permission("Organization", "read", organization): frappe.throw(_("Not permitted"), frappe.PermissionError)`. Apply same pattern to `get_equipment_by_organization()` and `get_equipment_by_person()`. |
| **P1-03** | Spec Compliance | jeni52 | **FR-013 Incomplete: Deactivation Not Blocked.** The spec requires blocking Org Member *deactivation* when equipment is assigned, but only `on_trash` is hooked. A user can set Org Member status to "Inactive" while equipment is still assigned, creating inconsistent data. | Register `check_equipment_assignments_on_member_removal()` on `Org Member.on_update` in hooks.py. Modify the function to also check when `status` changes away from "Active" and block if equipment is assigned. |
| **P1-04** | Security | jeni52 | **Hook Ordering Risk: Side Effects Before Validation.** In hooks.py, `remove_user_permissions` executes before `check_equipment_assignments_on_member_removal`. If the equipment check throws, you rely on transaction rollback to restore permissions—a fragile pattern. | In `dartwing/hooks.py:182-185`, reorder the `on_trash` list: `["dartwing.dartwing_core.doctype.equipment.equipment.check_equipment_assignments_on_member_removal", "dartwing.permissions.helpers.remove_user_permissions"]` (equipment check first). |
| **P1-05** | Security | jeni52 | **Create-Path Authorization Gap.** `validate_user_has_organization()` only checks if user has *any* Organization permission, not if they can create equipment for the *selected* `owner_organization`. A user with access to Org A can create equipment for Org B. | Replace `validate_user_has_organization()` with a check that verifies User Permission exists for `(user, allow="Organization", for_value=self.owner_organization)`. The `owner_organization` is already required, so validate specifically for that org. |
| **P2-01** | Maintainability | opus45, geni30, grokf1, jeni52, sonn45 | **Missing Unit Tests.** No test files exist for Equipment validation logic. Critical business rules (serial uniqueness, assignment validation, org deletion protection, permission filtering) have no regression coverage. | Create `dartwing/dartwing_core/doctype/equipment/test_equipment.py` with test cases for: (1) serial number uniqueness, (2) assignment requires org membership, (3) create without org access fails, (4) org deletion with equipment fails, (5) org member deactivation with assigned equipment fails. |
| **P2-02** | Maintainability | sonn45 | **Permission Function Naming Inconsistency.** Equipment uses `get_permission_query_conditions(user)` while all other DocTypes use `get_permission_query_conditions_{doctype}(user)` pattern (e.g., `get_permission_query_conditions_company`). This breaks convention and could cause conflicts if multiple doctypes share a module. | Rename functions in `dartwing/permissions/equipment.py` to `get_permission_query_conditions_equipment()` and `has_permission_equipment()`. Update references in `hooks.py` accordingly. |
| **P2-03** | Maintainability | opus45, jeni52 | **Redundant `validate_equipment_name()` Method.** The field is already marked `reqd: 1` in `equipment.json:39`. Frappe enforces required fields before the `validate` hook runs. This is duplicate code with no functional benefit. | Remove `validate_equipment_name()` method and its call in `validate()`. Let the DocType metadata handle required field enforcement (low-code philosophy). |
| **P2-04** | Performance | opus45, grokf1 | **Permission Query Fetches User Permissions on Every Request.** `get_permission_query_conditions_equipment()` calls `frappe.get_all("User Permission", ...)` for each request. For users with many org memberships, this adds latency. | Implement request-level caching: store result in `frappe.local.user_orgs_{user}` and reuse within the same request. Consider extracting to shared helper used by all permission modules. |
| **P2-05** | Data Integrity | sonn45 | **Missing Organization Immutability Validation.** `owner_organization` can be changed after equipment creation, potentially breaking permission assumptions and creating inconsistent assignment state (assigned person not in new org). Architecture implies ownership should be immutable. | Add `validate_owner_organization_immutable()` in `equipment.py` that throws if `owner_organization` changes on non-new documents. If transfers are needed, create a separate `transfer_equipment()` workflow method. |
| **P2-06** | Audit/Compliance | opus45, sonn45 | **No Explicit Audit Trail for Assignment Changes.** While `track_changes: 1` is enabled, there's no explicit logging when equipment is reassigned. For HIPAA/SOC2 compliance and custody tracking, assignment changes should be explicitly audited. | Add `on_update()` hook that checks `has_value_changed("assigned_to")` and logs via `self.add_comment("Info", f"Assignment changed from {old} to {new}")` or creates a dedicated audit record. |
| **P2-07** | Maintainability | geni30 | **Hardcoded Status Strings.** Status values ("Active", "In Repair", "Retired") are duplicated in equipment.py, equipment.json, and equipment.js. If a status is renamed, multiple files must be updated. | Define constants in `equipment.py` (e.g., `STATUS_ACTIVE = "Active"`) and use them in validation code. JSON and JS must remain strings, but Python code should reference constants for consistency. |
| **P2-08** | UX | opus45 | **Client Script: Poor UX When No Organization Selected.** When `owner_organization` is empty, `assigned_to` dropdown shows empty results via `name: ["in", []]` trick. User sees empty dropdown with no explanation. | Modify `set_assigned_to_query()` to disable `assigned_to` field and show description "Select organization first" when `owner_organization` is empty. Re-enable when org is selected. |
| **P2-09** | Feature Gap | sonn45 | **Missing Status Options: "Lost" and "Stolen".** Asset management systems typically track lost/stolen equipment for insurance, security reporting, and compliance (tracking devices with sensitive data). | Add "Lost" and "Stolen" to status options in `equipment.json:65`. Optionally add conditional fields `incident_date` and `incident_notes` with `depends_on: "eval:doc.status=='Lost' || doc.status=='Stolen'"`. |
| **P2-10** | Data Integrity | sonn45 | **Missing Location Validation.** `current_location` (Link to Address) has no validation to ensure the address is associated with the `owner_organization`. Equipment could be assigned to addresses from unrelated organizations. | Add `validate_current_location()` method that checks if Address has a Dynamic Link to the equipment's organization. Use `frappe.msgprint()` (warning) rather than `frappe.throw()` to allow flexibility for shared locations. |
| **P3-01** | Maintainability | opus45 | **Inaccurate Child Table Docstrings.** `EquipmentMaintenance` docstring mentions "description" field but actual field is "task". Minor documentation inconsistency. | Update docstring in `equipment_maintenance.py` to accurately reflect field names. |
| **P3-02** | Extensibility | sonn45 | **Hardcoded Document Types in Child Table.** Equipment Document types are hardcoded Select options. Users cannot add custom types without code changes. | Consider creating a separate `Equipment Document Type` DocType with Link field, or at minimum add a `document_type_description` Data field with `depends_on: "eval:doc.document_type=='Other'"` for custom types. |
| **P3-03** | Future Feature | sonn45 | **Maintenance Schedule Has No Automation.** The maintenance child table captures `next_due` dates but nothing monitors overdue tasks or sends notifications. Schedule is informational only. | Plan for future: Add scheduled job in `scheduler_events.daily` to check for overdue maintenance and create notifications. Consider Equipment Maintenance Record DocType to track completed maintenance. |
| **P3-04** | UX | sonn45 | **Missing Field Descriptions.** Fields like `serial_number`, `current_location`, `assigned_to` lack descriptions. Users may be uncertain about their purpose or expected values. | Add `"description"` attribute to key fields in `equipment.json` explaining their purpose (e.g., "Manufacturer's serial number. Must be globally unique."). |
| **P3-05** | Architecture | opus45, jeni52 | **API Helpers in DocType Controller.** `get_equipment_by_organization()` and `get_equipment_by_person()` are API-style endpoints in the DocType controller. Project guidelines suggest whitelisted endpoints live under `dartwing/api/`. | Consider moving API helpers to `dartwing/api/equipment.py` for cleaner separation. DocType controllers should focus on document lifecycle. (Low priority—current location works.) |
| **P3-06** | Performance | geni30, grokf1 | **Consider Adding Database Index.** Ensure `owner_organization`, `assigned_to`, `status`, `equipment_type` fields have indexes for query performance at scale (1000+ items per org per SC-002). | Verify indexes exist via `bench migrate`. Consider adding `search_index: 1` to frequently filtered fields in JSON if not already present. |

---

## 2. Summary & Architect Decision Log

### Synthesis Summary

The Equipment DocType implementation is **fundamentally sound** and demonstrates strong understanding of Frappe patterns and the Dartwing polymorphic architecture. All five reviewers praised the validation logic, permission model design, cascade deletion protection, and client-side UX enhancements. However, **five P1 security/compliance issues** must be resolved before merge:

1. **SQL injection vulnerability** in permission query (double-quoting breaks escaping)
2. **Cross-tenant data exposure** in `get_org_members()` API method
3. **Spec non-compliance** for FR-013 (deactivation not blocked, only deletion)
4. **Hook ordering risk** that could leave permissions in inconsistent state
5. **Authorization gap** allowing equipment creation for unauthorized organizations

After addressing these critical issues, the remaining P2/P3 items focus on maintainability (tests, naming consistency, redundant code), performance (caching, indexing), and feature completeness (additional statuses, audit trails, field descriptions).

### Conflict Resolution Log

| Conflict | Reviewers | Resolution | Justification |
|:---------|:----------|:-----------|:--------------|
| **SQL Injection Severity** | opus45 rated LOW (escape provides protection), jeni52/sonn45 rated CRITICAL (double-quoting breaks escape) | **Resolved as P1-CRITICAL** | jeni52 and sonn45 correctly identified that `frappe.db.escape()` returns already-quoted strings. Adding additional quotes (`f"'{...}'"`) breaks the escaping mechanism entirely. Per `dartwing_core_arch.md` Section 8.3 Security Architecture, SQL injection is a compliance violation. The fix in `company.py` (CR-001 FIX comment) confirms the correct pattern. |
| **Unit Tests Priority** | geni30 rated HIGH/blocker, opus45/grokf1/sonn45 rated MEDIUM/future debt | **Resolved as P2-HIGH** | Per `.specify/memory/constitution.md` Section 6 ("Tests required for business logic"), tests are expected but not strictly blocking merge. The feature can be merged with tests as immediate follow-up, but tests should be completed before the next feature branch. |
| **Redundant Validation** | jeni52 suggested removing both `validate_equipment_name` AND `validate_serial_number_unique` (rely on metadata), opus45/geni30 suggested keeping serial validation for better UX | **Keep serial validation, remove name validation** | Per `dartwing_core_arch.md` low-code philosophy, required fields should use `reqd: 1` metadata. However, uniqueness errors from database constraints produce less user-friendly messages than Python validation with `frappe.throw()`. Keep serial validation for UX, remove redundant required-field validation. |
| **Permission Naming Convention** | sonn45 rated HIGH, others did not flag | **Resolved as P2-MEDIUM** | This is a naming convention issue, not a functional bug. The code works correctly. However, per constitution.md Section 7 Naming Conventions, consistency is expected. Fix should be made but does not block merge. |
| **Hardcoded Values (Status/Doc Types)** | geni30 rated HIGH (status strings), sonn45 rated MEDIUM (doc types) | **Resolved as P2/P3** | Status string duplication is a maintainability issue (P2-07) but not critical. Document type extensibility is a nice-to-have (P3-02). Per low-code philosophy, prefer Link to master DocType long-term, but current implementation is acceptable for MVP. |
| **Audit Trail Implementation** | opus45 suggested `frappe.logger()`, sonn45 suggested `self.add_comment()` or dedicated DocType | **Recommend `self.add_comment()` for MVP** | Per `dartwing_core_arch.md` Section 8.1 (Audit Logging), comprehensive activity logging is required for compliance. The `add_comment()` approach provides immediate visibility in the document timeline without requiring a new DocType. Dedicated Equipment Assignment Log can be added later if more structured reporting is needed. |

---

## Appendix: Files Requiring Changes

### P1 Critical Fixes (Required Before Merge)

| File | Lines | Change |
|:-----|:------|:-------|
| `dartwing/permissions/equipment.py` | 46 | Remove extra quotes from `frappe.db.escape()` |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | 136-152 | Add org permission check before `get_org_members()` SQL |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | 156, 187 | Add permission checks to `get_equipment_by_*()` methods |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | 231-253 | Extend to check status changes, not just deletion |
| `dartwing/hooks.py` | 180-187 | Add `on_update` hook for Org Member; reorder `on_trash` list |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | 93-116 | Fix authorization to check specific `owner_organization` |

### P2 Improvements (Should Fix Soon)

| File | Change |
|:-----|:-------|
| `dartwing/dartwing_core/doctype/equipment/test_equipment.py` | Create new file with unit tests |
| `dartwing/permissions/equipment.py` | Rename functions to include `_equipment` suffix |
| `dartwing/hooks.py` | Update permission function references |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | Remove `validate_equipment_name()` |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | Add `validate_owner_organization_immutable()` |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | Add `on_update()` for assignment audit trail |
| `dartwing/dartwing_core/doctype/equipment/equipment.js` | Improve empty-org UX for `assigned_to` field |
| `dartwing/dartwing_core/doctype/equipment/equipment.json` | Add "Lost" and "Stolen" status options |

---

**End of Master Plan**
