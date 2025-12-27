# Change: Upgrade Dartwing Frappe compatibility to v16

## Why
Dartwing needs to align with Frappe/ERPNext v16 to avoid dependency conflicts and keep the stack on a supported, stable release line.

## What Changes
- **BREAKING**: Target Frappe v16 as the supported backend version for Dartwing.
- Update Dartwing app dependencies, docs, and bench setup guidance to reference v16.
- Audit and update any deprecated Frappe APIs used by Dartwing.
- Create a `v16` branch for ongoing compatibility work.

## Impact
- Affected specs: `frappe-version-support`
- Affected code: `pyproject.toml`, `dartwing/`, `docs/`, `README.md`, `SETUP.md`, and bench-related scripts or references
