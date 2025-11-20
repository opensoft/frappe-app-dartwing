# Dartwing

Backend and family management app for Frappe.

## Data model
- **Family**: family_name, slug, description, tags, contact_email/phone, status, created_date, members (child table)
- **Family Member** (child table): full_name, relationship, email, phone, date_of_birth, status, notes

## APIs (dartwing.api.v1)
- `create_family(family_name, description=None, status="Active", members=None)`
- `get_family(name)` / `get_all_families(filters=None, fields=None, limit_start=0, limit_page_length=20)`
- `update_family(name, **kwargs)` / `delete_family(name)`
- `search_families(query, limit=20)` / `get_family_stats()`
- Member ops: `add_family_member`, `update_family_member`, `delete_family_member`

## Setup
- Install app on site: `bench --site SITE install-app dartwing`
- Migrate doctypes/fixtures: `bench --site SITE migrate`
- Family Manager role fixture included (fixtures/role.json)

## Tests
- See `tests/test_family_api.py` (skipped by default; requires site context).
