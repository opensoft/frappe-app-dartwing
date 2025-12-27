## ADDED Requirements
### Requirement: Frappe v16 Compatibility
The Dartwing app SHALL install, migrate, and run on Frappe v16 with ERPNext v16.

#### Scenario: Fresh install on v16 bench
- **WHEN** a new bench is initialized with Frappe v16 and Dartwing is installed
- **THEN** `bench migrate` completes without errors and the app loads without runtime exceptions

#### Scenario: Test suite on v16
- **WHEN** `bench --site <site> run-tests --app dartwing` is executed on a v16 bench
- **THEN** the Dartwing test suite completes without failures attributable to deprecated APIs
