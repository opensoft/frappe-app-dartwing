<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# dartwing Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-01

## Active Technologies
- Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.fixtures (002-role-template-doctype)
- MariaDB 10.6+ via Frappe ORM (002-role-template-doctype)
- Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.permissions (005-user-permission-propagation)
- MariaDB 10.6+ (via Frappe ORM) (005-user-permission-propagation)

- Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.background_jobs (001-person-doctype)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11+ (Frappe 15.x backend): Follow standard conventions

## Recent Changes
- 005-user-permission-propagation: Added Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.permissions
- 002-role-template-doctype: Added Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.fixtures

- 001-person-doctype: Added Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.background_jobs

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
