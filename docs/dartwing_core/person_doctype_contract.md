# Person Doctype Contract

**Purpose:** Canonical definition of `Person`, identity linkage, and permission propagation.

## Schema (required fields)
- `primary_email` (Data, reqd, unique)
- `keycloak_user_id` (Data, unique, nullable for lite/local auth)
- `frappe_user` (Link → User, unique when set)
- `first_name`, `last_name` (Data)
- `mobile_no` (Data, optional, country-aware validation)
- `personal_org` (Link → Organization, created at signup for personal identity)
- PII/privacy flags: `is_minor` (Check), `consent_captured` (Check), `consent_timestamp` (Datetime)
- Audit: `source` (Select: signup/invite/import), `status` (Select: Active/Inactive/Merged)

## Constraints
- Enforce uniqueness: `primary_email`, `keycloak_user_id`, `frappe_user`.
- Prevent deletion when linked to Org Member; use deactivate/merge instead.
- On insert, if `keycloak_user_id` present and no `frappe_user`, auto-create Frappe User with default roles (`Dartwing User`) when allowed by site config.

## Flows
### Signup (personal)
1. Keycloak signup → callback provides `email`, `sub`.
2. Create Person with `primary_email`, `keycloak_user_id`; create `frappe_user` if configured.
3. Create personal `Organization` (org_type = Family) and link via `personal_org`.
4. Add Org Member for personal org; add `User Permission` for that org.

### Invitation to Business Org
1. Org Admin invites email.
2. Lookup Person by `primary_email`; if missing, create stub Person with status=Pending and send Keycloak invite.
3. On accept, set `keycloak_user_id` (if not set), map/create `frappe_user`, add Org Member + `User Permission`.

### Merge
- If duplicate Persons detected (same email/Keycloak), merge: re-link Org Members, audit the merge, soft-delete loser.

## Permission Propagation
- Org Member creation must create `User Permission` for Organization and any concrete doctypes (via `user_permission_doctypes`).
- Shared helper (API + Socket.IO + jobs) should enforce org scoping using `User Permission`.
- When roles synced from Keycloak groups, ensure fallback role mapping (default to `Dartwing User`) and log failures.

## Tests (minimum)
- Insert Person with duplicate `primary_email` → fails.
- Insert Person with `keycloak_user_id` auto-creates Frappe User when enabled.
- Invitation flow adds Org Member and User Permission for target org.
- Permission filters restrict multi-org users to allowed orgs in list views and custom RPCs.
