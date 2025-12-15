# Claude Instructions

<instructions>
You are working in a local development environment. When you need to interact with external services (like GitHub, Firebase, etc.) where both a Command Line Interface (CLI) tool and a Model Context Protocol (MCP) server are available, **always prefer using the Bash tool to run the CLI command first**.

Only fall back to using the MCP server if the CLI execution fails or the CLI tool does not have the necessary capability for the task.
</instructions>

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
- Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.utils.logger (004-org-bidirectional-hooks)
- Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.background_jobs, Redis/RQ, Socket.IO (011-background-job-engine)
- MariaDB 10.6+ via Frappe ORM (job metadata persistence) (011-background-job-engine)

### Core Stack
- Python 3.11+ (Frappe 15.x backend)
- Frappe Framework 15.x, frappe.model.document
- MariaDB 10.6+ via Frappe ORM

### Feature-Specific Modules
- frappe.fixtures (002-role-template-doctype)
- frappe.permissions (005-user-permission-propagation)
- frappe.background_jobs (001-person-doctype)

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
- 011-background-job-engine: Added Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.background_jobs, Redis/RQ, Socket.IO
- 009-api-helpers: Added Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.permissions
- 007-equipment-doctype: Added Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.fixtures
- 006-company-doctype: Added Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.fixtures
- 005-user-permission-propagation: Added Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.permissions
- 004-org-bidirectional-hooks: Added Python 3.11+ (Frappe 15.x backend) + Frappe Framework 15.x, frappe.model.document, frappe.utils.logger


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
