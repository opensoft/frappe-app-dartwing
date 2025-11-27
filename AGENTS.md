# Repository Guidelines

## Project Structure & Modules
- Root docs (`README.md`, `API.md`, `BUSINESS_LOGIC.md`, `STRUCTURE.md`) describe behavior; code lives in `dartwing/`.
- Key packages: `dartwing/api/` (whitelisted endpoints), `dartwing/doctype/` (DocTypes and controllers), `dartwing/integrations/` (service connectors), `dartwing/utils/` (shared helpers), `dartwing/patches/` (+ `patches.txt` for migration order), and `dartwing/tests/` for app-level tests.
- Frontend/public assets sit in `public/`, server-rendered templates in `templates/`, and static pages in `www/`. Fixtures live in `fixtures/`.
- Prefer placing business logic per `BUSINESS_LOGIC.md` (DocType controllers for document rules, utils for reuse, API modules thin).

## Build, Test, and Development Commands
- Install to a site: `bench --site <site> install-app dartwing`; apply schema changes with `bench --site <site> migrate`.
- Run the stack locally with `bench start` from your bench; use a test site for development.
- Execute tests with Frappe context: `bench --site <site> run-tests --app dartwing`. Direct `pytest` works only when Frappe is importable and a site is configured.
- Export/import fixtures when needed: `bench --site <site> export-fixtures` / `bench --site <site> import-fixtures`.

## Coding Style & Naming Conventions
- Python 3.10; follow PEP 8 with 4-space indents and type hints where helpful. Keep Frappe scaffolded tabs only when modifying existing tab-indented blocks.
- Whitelisted API functions use `snake_case` and live under `dartwing.api.<module>`. DocType controllers stay in `dartwing/doctype/<name>/<name>.py` and keep validation/business logic close to the model.
- Keep modules focused and composable; use `_()` for user-facing strings and log via `frappe.log_error` on failures.

## Testing Guidelines
- Tests use `pytest` with Frappe fixtures; site context is required (current tests are skipped without it). Name files `tests/test_<area>.py`.
- Cover new endpoints and DocType logic with happy-path and failure cases. Clean up created documents inside tests to keep sites reusable.

## Commit & Pull Request Guidelines
- Match existing history: short, imperative subjects (e.g., `fix: update modules.txt`, `Update configuration and remove root __init__.py`); group related changes per commit.
- PRs should include: what changed and why, site/bench notes if migrations or fixtures are added, tests run (`bench --site <site> run-tests --app dartwing`), and any screenshots for UI-facing assets.

## Security & Configuration
- Never commit credentials. Service endpoints/API keys belong in the site config (see README example JSON) or environment-managed secrets.
- Keep fixtures and sample data sanitized; avoid embedding production-like data. When adding migrations, append to `dartwing/patches.txt` in execution order.
