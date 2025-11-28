# Dartwing Core Architecture Critique

**Focus: Organization Document**

---

## Executive Summary

The Organization doctype attempts to serve as a "universal" entity representing families, companies, nonprofits, and clubs within a single table structure. While this approach offers some development velocity benefits, it introduces significant architectural concerns that may impact long-term maintainability, performance, and data integrity.

---

## 1. Strengths of the Current Design

### 1.1 Development Simplicity
- Single doctype reduces initial development complexity
- Shared CRUD operations across all organization types
- Unified API endpoints simplify client integration

### 1.2 Frappe Alignment
- Leverages `depends_on` for conditional field visibility effectively
- Child tables (Officers, Members, Tiers) are well-structured
- Standard Frappe permission model is preserved

### 1.3 Flexibility
- New organization types could theoretically be added via the `org_type` Select field
- Common fields (name, status, logo) are genuinely shared

---

## 2. Critical Concerns

### 2.1 Single Table Inheritance Anti-Pattern

The Organization doctype exhibits the "Single Table Inheritance" pattern, which is widely considered an anti-pattern at scale:

**Problems:**
- **Sparse data**: A Family record will have NULL values for `tax_id`, `registered_agent`, `entity_type`, `jurisdiction_country`, etc. A Company will have NULL for `family_nickname`, `primary_residence`, `membership_tiers`
- **Index inefficiency**: Queries filtering by `org_type` cannot leverage type-specific indexes effectively
- **Validation complexity**: Business rules become conditional (`if org_type == 'Company': validate_ein()`)
- **Schema evolution**: Adding fields for one type bloats all records

**Estimated NULL percentage per org_type:**
| org_type | Estimated NULL field percentage |
|----------|--------------------------------|
| Family | ~60% of defined fields unused |
| Company | ~40% of defined fields unused |
| Nonprofit | ~45% of defined fields unused |
| Club | ~55% of defined fields unused |

### 2.2 Missing Data Integrity Constraints

The design lacks proper referential integrity for type-specific relationships:

```
PROBLEM: Nothing prevents a "Family" organization from having:
- Organization Officers (which makes no semantic sense)
- Organization Member Partners with ownership percentages
- A registered_agent reference
```

The `depends_on` attribute only controls **UI visibility**, not database-level constraints. A malformed API call could insert invalid data.

**Recommendation:** Add server-side validation in `before_save` hooks or consider type-specific child doctypes.

### 2.3 Org Member Role Ambiguity

The `Org Member` doctype links to a generic `Role Template` that must filter by `applies_to_org_type`. This creates:

1. **Query overhead**: Every role lookup requires org_type filtering
2. **Potential misassignment**: No FK constraint prevents assigning a "Parent" role to a Company org
3. **UI complexity**: Role dropdowns must dynamically filter options

**Current flow:**
```
Person → Org Member → Role Template (filtered by org_type)
                  ↓
              Organization
```

**Better approach:**
```
Person → [FamilyMember | Employee | ClubMember | BoardMember]
                              ↓
              [Family | Company | Club | Nonprofit]
```

### 2.4 Missing Hierarchical Organization Support

The current model has no support for:
- Parent/subsidiary company relationships
- Franchise structures
- Multi-chapter nonprofits
- Extended family networks

**Missing field:**
```json
{
  "fieldname": "parent_organization",
  "label": "Parent Organization",
  "fieldtype": "Link",
  "options": "Organization"
}
```

This is a significant omission for real-world corporate structures.

### 2.5 Address Handling Inconsistency

Three separate address fields exist:
- `registered_address` (Companies)
- `physical_address` (Companies)
- `primary_residence` (Families)

**Issues:**
- No standardized address management across types
- Missing: mailing address, billing address, secondary residences
- The `Address` doctype is not shown but assumed to exist

---

## 3. Performance Concerns

### 3.1 Query Patterns

Common queries will suffer from the polymorphic design:

```python
# Inefficient: Scanning all organizations to find companies
frappe.get_all("Organization", filters={"org_type": "Company"})

# Would be more efficient with dedicated Company doctype
frappe.get_all("Company")
```

### 3.2 Recommended Indexes

If the current design is retained, these indexes are critical:
```sql
CREATE INDEX idx_org_type ON tabOrganization(org_type);
CREATE INDEX idx_org_status_type ON tabOrganization(status, org_type);
CREATE INDEX idx_org_jurisdiction ON tabOrganization(jurisdiction_country, jurisdiction_state);
```

### 3.3 Scaling Projections

| Organization Count | Expected Issues |
|-------------------|-----------------|
| < 10,000 | Minimal impact |
| 10,000 - 100,000 | Query latency increases, index tuning required |
| > 100,000 | Single table becomes bottleneck, sharding complexity |

---

## 4. Alternative Architecture Proposals

### 4.1 Option A: Abstract Base + Concrete Types (Recommended)

```
Organization (abstract/virtual - shared fields only)
    ├── Family (extends Organization)
    ├── Company (extends Organization)
    ├── Nonprofit (extends Organization)
    └── Club (extends Organization)
```

**Implementation in Frappe:**
- Create separate doctypes: `Family`, `Company`, `Nonprofit`, `Club`
- Use shared validation utilities
- Create a virtual "Organization" view for cross-type queries

### 4.2 Option B: Organization + Type-Specific Extension Tables

```
Organization (core fields)
    ├── Organization Legal Entity (Company/Nonprofit details)
    ├── Organization Family Details (Family-specific)
    └── Organization Club Details (Club-specific)
```

This is the "Class Table Inheritance" pattern - more normalized but requires joins.

### 4.3 Option C: Keep Current + Strict Validation Layer

If refactoring is not feasible:
1. Add `validate()` method with type-specific rules
2. Create type-specific wrapper APIs (`create_family()`, `create_company()`)
3. Implement database triggers for constraint enforcement
4. Add comprehensive audit logging for data integrity monitoring

---

## 5. Security Considerations

### 5.1 Permission Boundary Leakage

The current permission model shows:
```json
{ "role": "Organization Admin", "read": 1, "write": 1, "create": 1 }
```

**Concern:** An "Organization Admin" of a Family could potentially view/modify Company-type organizations if document-level permissions aren't configured.

**Recommendation:** Implement user_permission rules tied to specific organization records.

### 5.2 Sensitive Field Exposure

Company-type fields like `tax_id`, `beneficial_owners`, and `capital_contribution` are sensitive. The architecture doesn't indicate:
- Field-level encryption
- Audit logging for sensitive field access
- Role-based field visibility (beyond UI hiding)

---

## 6. Recommendations Summary

| Priority | Recommendation |
|----------|---------------|
| High | Add server-side validation for type-specific constraints |
| High | Implement parent_organization for hierarchical support |
| High | Create indexes for org_type-based queries |
| Medium | Consider splitting into type-specific doctypes for new installations |
| Medium | Add field-level audit logging for sensitive data |
| Medium | Implement document-level permissions per organization |
| Low | Create migration path from universal to type-specific model |
| Low | Add address standardization across org types |

---

## 7. Conclusion

The "Universal Organization" approach is pragmatic for a v1 product seeking rapid market validation. However, the architecture document should acknowledge these trade-offs explicitly and include a migration path toward a more normalized model as the platform scales.

The current design will work for:
- Small deployments (< 10,000 organizations)
- Use cases where most organizations are a single type
- Teams comfortable with heavy validation layer maintenance

The current design will struggle with:
- Large-scale multi-tenant deployments
- Complex reporting across organization types
- Strict compliance requirements (HIPAA, SOC 2 audits)
- Type-specific feature velocity (each type evolves differently)

---

*Critique prepared: November 2025*
