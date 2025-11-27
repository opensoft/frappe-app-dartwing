# TechSpec – Dartwing Company & Multi-Company System

**Version:** 1.0 (November 2025) – Production Complete  
**Stack:** Frappe 15 + Keycloak 24 + PostgreSQL + Redis + S3

## Core DocTypes & Relationships

| DocType                | Type       | Key Fields (selected)                                                                                                                                                                                      | Links / Child Tables                                                                                 |
| ---------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Company**            | Core       | Friendly Name, Legal Name, Short Code (auto), Logo, Primary Color, EIN, NAICS, Industry Vertical, Billing Plan, Stripe Customer ID, Custom Domain, Data Residency Region, Status (Active/Suspended), Owner | Company Address, Company Tax ID, Company Domain, Company Phone, Company Department, Company Location |
| **Company Member**     | Child/Link | Company → User, Role (Owner/Admin/Member/Accountant/Viewer), Invited By, Accepted On                                                                                                                       | –                                                                                                    |
| **Company Invitation** | Standalone | Company, Email (lowercase), Role, Token (UUIDv4), Expires On (30 days), Status (Pending/Accepted/Expired)                                                                                                  | –                                                                                                    |
| **Company Address**    | Child      | Address (Link to global Address), Type (Mailing/Physical/Legal/Billing/etc.), Is Primary                                                                                                                   | –                                                                                                    |

## Detailed User & Company Flows

| Flow                              | Implementation Details                                                                                                                                | Latency Target |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| Create Company                    | Standard form → On submit: insert Company + Company Member (role=Owner) → set `frappe.local.company`                                                  | <2s            |
| Invite Member                     | Role ≥ Admin → create Company Invitation → generate UUID token → send templated email via Frappe Email Queue (MJML template)                          | <3s            |
| Accept Invitation (Existing User) | Public route `/accept-invite?token=xxx` → validate token → if logged in → insert Company Member → redirect to dashboard with success message          | <1s            |
| Accept Invitation (New User)      | Token embedded in signup URL → after Keycloak OIDC redirect → server method consumes token → creates User (if needed) + Company Member                | <4s total      |
| Company Switcher                  | Top bar Vue component → API `/api/method/dartwing.core.switch_company` → sets Redis session key + `frappe.local.company` for entire request lifecycle | <400ms         |
| Permissions & Row-Level Security  | All business DocTypes have server-side check: `if doc.company != frappe.local.company: throw PermissionError`                                         | –              |
| White-Label & Custom Domain       | CNAME → Nginx → bench routing → Company.custom_domain resolved → inject Company logo/color/email footer globally                                      | –              |
| Billing & Metering                | All metered events (fax pages, storage, API calls) write to `Company Usage Log` → aggregated nightly → Stripe metered billing                         | –              |

## Complete Company Data Model (180+ fields – grouped)

### Basic & Branding

Friendly Name • Legal Name • Short Code • Logo • Favicon • Primary Color • Website • Email Footer HTML • Abbreviations/DBA

### Addresses (Child Table)

Type (Mailing/Physical/Legal/Billing/Shipping/Registered) • Full Address • Is Primary

### Legal & Tax

Entity Type • State/Country of Incorporation • EIN (masked) • VAT/GSTIN (multi-country) • DUNS • Tax Exempt + Certificate

### Industry & Compliance

Primary NAICS • Industry Vertical (Healthcare, Legal, etc.) • Regulated Flags (HIPAA, FINRA, GDPR) • Signed BAA • Default Retention Years

### Contacts & Support

General Phone • Toll-Free • General/Support/Sales/Billing Email • Emergency Contact

### SSO & Identity

Identity Provider • IdP Realm/Tenant • SCIM 2.0 Enabled • Custom SAML Entity ID

### Billing & Plan

Billing Plan • Stripe Customer ID • Billing Contact/Address • Tax Exempt Status

### White-Label & System

Custom Domain • Custom Email Domain • Remove Dartwing Branding • Company Status • Data Residency Region

### Structure (optional toggles)

Enable Departments • Enable Locations/Branches

## Key Server Methods (frappe.whitelisted)

```python
dartwing.core.doctype.company.company.create_company(name, legal_name, ...)
dartwing.core.doctype.company_invitation.company_invitation.send_invitation(company, email, role)
dartwing.core.page.accept_invite.accept_invite.validate_and_join(token)
dartwing.core.api.switch_company(company_name)
dartwing.core.doctype.company.company.transfer_ownership(company, new_owner_user)
dartwing.core.doctype.company.company.suspend_company(company)
dartwing.core.doctype.company.company.export_all_data(company)  # GDPR
```
