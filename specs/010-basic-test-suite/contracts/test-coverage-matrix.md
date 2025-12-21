# Test Coverage Matrix

**Feature**: 010-basic-test-suite
**Date**: 2025-12-14

## Functional Requirements Coverage

This matrix maps each functional requirement from the spec to specific test cases.

### FR-001: Person DocType Tests

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| `test_duplicate_email_rejected` | test_person.py | Email uniqueness constraint | EXISTS |
| `test_nullable_unique_keycloak_user_id_duplicate_rejected` | test_person.py | Keycloak ID uniqueness | EXISTS |
| `test_deletion_blocked_with_org_member` | test_person.py | Deletion prevention | EXISTS |
| `test_deletion_allowed_without_org_member` | test_person.py | Deletion success | EXISTS |

### FR-002: Organization Hooks Tests

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| `test_us1_org_type_family_creates_family_record` | test_organization_hooks.py | Auto-create Family | EXISTS |
| `test_us1_org_type_company_creates_company_record` | test_organization_hooks.py | Auto-create Company | EXISTS |
| `test_us1_concrete_type_organization_field_points_back` | test_organization_hooks.py | Bidirectional link | EXISTS |
| `test_us3_delete_org_cascades_to_family` | test_organization_hooks.py | Cascade delete | EXISTS |
| `test_us4_changing_org_type_raises_error` | test_organization_hooks.py | Type immutability | EXISTS |

### FR-003: Org Member Tests

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| `test_org_member_uniqueness` | test_org_member.py | Person+org unique constraint | EXISTS |
| `test_role_filtered_by_org_type` | test_org_member.py | Role filtering | NEW |
| `test_role_org_type_mismatch_rejected` | test_org_member.py | Cross-type role validation | NEW |

### FR-004: Permission Propagation Tests

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| `test_create_permissions_active_member` | test_permission_propagation.py | Auto-create permissions | EXISTS |
| `test_remove_permissions_on_delete` | test_permission_propagation.py | Auto-remove permissions | EXISTS |
| `test_status_change_active_to_inactive` | test_permission_propagation.py | Permission removal on status change | EXISTS |

### FR-005: Permission Filtering Tests

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| `test_list_view_filtered_by_user_permission` | test_permission_helpers.py | List filtering | EXISTS |
| `test_single_document_access_denied` | test_permission_helpers.py | Document access control | EXISTS |

### FR-006: API Helper Tests

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| `test_get_concrete_doc_returns_document` | test_organization_hooks.py | get_concrete_doc API | EXISTS |
| `test_get_organization_with_details_returns_merged_data` | test_organization_hooks.py | get_organization_with_details | EXISTS |
| `test_get_user_organizations_returns_accessible_orgs` | test_api_helpers.py | get_user_organizations | NEW |
| `test_get_user_organizations_excludes_unauthorized` | test_api_helpers.py | Permission enforcement | NEW |
| `test_get_org_members_returns_active_members` | test_api_helpers.py | get_org_members | NEW |
| `test_get_org_members_permission_denied` | test_api_helpers.py | Permission enforcement | NEW |

### FR-007: OrganizationMixin Tests

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| `test_org_name_property_returns_parent_value` | test_organization_mixin.py | org_name accessor | NEW |
| `test_logo_property_returns_parent_value` | test_organization_mixin.py | logo accessor | NEW |
| `test_org_status_property_returns_parent_value` | test_organization_mixin.py | org_status accessor | NEW |
| `test_get_organization_doc_returns_full_document` | test_organization_mixin.py | Document retrieval | NEW |
| `test_update_org_name_modifies_parent` | test_organization_mixin.py | Name update method | NEW |

### FR-008: Test Isolation

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| Verified by pattern | All test files | setUp/tearDown cleanup | EXISTS |

### FR-009: Command Line Execution

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| N/A | bench run-tests | CLI execution support | EXISTS |

### FR-010: Clear Failure Messages

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| Verified by implementation | All test files | Descriptive assertions | EXISTS |

### FR-011: Negative Test Cases

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| `test_duplicate_email_rejected` | test_person.py | Invalid input rejection | EXISTS |
| `test_us1_invalid_org_type_rejected` | test_organization_hooks.py | Invalid type rejection | EXISTS |
| `test_get_org_members_permission_denied` | test_api_helpers.py | Unauthorized access | NEW |

### FR-012: Role Template Seed Data Tests

| Test Case | File | Description | Status |
|-----------|------|-------------|--------|
| `test_family_roles_exist` | test_role_template.py | Family seed data | NEW |
| `test_company_roles_exist` | test_role_template.py | Company seed data | NEW |
| `test_nonprofit_roles_exist` | test_role_template.py | Nonprofit seed data | NEW |
| `test_association_roles_exist` | test_role_template.py | Association seed data | NEW |

---

## Coverage Summary

| Status | Count | Percentage |
|--------|-------|------------|
| EXISTS | 25 | ~68% |
| NEW | 12 | ~32% |
| **Total** | **37** | **100%** |

---

## User Story Coverage

| User Story | Priority | Test Cases | Coverage |
|------------|----------|------------|----------|
| US1: Core Data Integrity | P1 | 4 EXISTS | Complete |
| US2: Organization Lifecycle | P1 | 5 EXISTS | Complete |
| US3: Permission Propagation | P1 | 3 EXISTS | Complete |
| US4: Role-Based Filtering | P2 | 2 NEW | Pending |
| US5: Org Member Uniqueness | P2 | 1 EXISTS | Complete |
| US6: API Helpers | P2 | 2 EXISTS, 4 NEW | Partial |
| US7: OrganizationMixin | P3 | 5 NEW | Pending |

---

## Success Criteria Validation

| Criterion | Test Approach | Status |
|-----------|---------------|--------|
| SC-001: 100% pass rate | All tests execute | Automated |
| SC-002: 80% coverage | Coverage matrix | 68% EXISTS + 32% NEW = 100% |
| SC-003: Module independence | No cross-module deps | Design constraint |
| SC-004: <5 min execution | bench run-tests timing | Automated |
| SC-005: Zero flakiness | 10 consecutive runs | Manual verification |
| SC-006: Regression detection | Existing tests fail on change | Implicit |
| SC-007: Clear error messages | Descriptive assertions | Review |
