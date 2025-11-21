# Dartwing

Backend and family management app for Frappe with multi-service integration.

## Overview

`frappe-app-dartwing` is a custom application layer built on top of the Frappe framework providing:

- **Family management** with comprehensive business logic
- **Multi-service integration** via proxy/connector patterns for:
  - ERPNext accounting module
  - Frappe Health healthcare management
  - Frappe Drive document management
- **Clean architectural separation** between custom code and third-party services

## Data Model

- **Family**: family_name, slug, description, tags, contact_email/phone, status, created_date, members (child table)
- **Family Member** (child table): full_name, relationship, email, phone, date_of_birth, status, notes

## APIs (dartwing.api.v1)

- `create_family(family_name, description=None, status="Active", members=None)`
- `get_family(name)` / `get_all_families(filters=None, fields=None, limit_start=0, limit_page_length=20)`
- `update_family(name, **kwargs)` / `delete_family(name)`
- `search_families(query, limit=20)` / `get_family_stats()`
- Member operations: `add_family_member`, `update_family_member`, `delete_family_member`

## Setup

### Prerequisites

- Frappe Framework installed and running
- Python 3.10+
- Optional: ERPNext, Frappe Health, Frappe Drive services for extended functionality

### Installation

```bash
# Clone the repository
git clone https://github.com/opensoft/frappe-app-dartwing.git
cd frappe-app-dartwing

# Install app on site
bench --site SITE install-app dartwing

# Run migrations
bench --site SITE migrate
```

### Configuration

Configure service connections in your Frappe site configuration (optional):

```json
{
  "erpnext_url": "http://erpnext-service:8000",
  "erpnext_api_key": "your-api-key",
  "erpnext_api_secret": "your-api-secret",
  
  "health_url": "http://health-service:8000",
  "health_api_key": "your-api-key",
  "health_api_secret": "your-api-secret",
  
  "drive_url": "http://drive-service:8000",
  "drive_api_key": "your-api-key",
  "drive_api_secret": "your-api-secret"
}
```

## Architecture

This application follows a service-oriented architecture with multiple proxy connectors:

```
┌─────────────────────────────────────────┐
│ frappe-app-dartwing Application         │
├─────────────────────────────────────────┤
│ Custom Features & Business Logic         │
│ Frappe Integration Layer                 │
│ Multi-Service Proxy/Connector Pattern    │
└────────────┬────────────────────────────┘
             │
             ├─→ (HTTP/RPC) → ERPNext (GPL-3.0)
             ├─→ (HTTP/RPC) → Frappe Health (GPL-3.0)
             ├─→ (HTTP/RPC) → Frappe Drive (AGPL-3.0)
             └─→ (Library)  → Frappe Framework (MIT)
```

### Key Architectural Principles

1. **No Third-Party Code Embedding**: This application does not include, modify, or redistribute source code from integrated services
2. **API-Based Integration**: Communication with services happens exclusively via HTTP/RPC API calls
3. **Service Separation**: Each service runs as an independent deployment with its own license terms
4. **Proxy Pattern**: The application acts as a proxy/connector forwarding requests to services
5. **Modular Connectors**: Each service has its own connector module for clean separation

## Tests

- See `tests/test_family_api.py` (skipped by default; requires site context)
- Family Manager role fixture included (fixtures/role.json)

## Contributing

Contributions are welcome! Please ensure:

- Service integrations remain as pure proxies (no code modifications)
- Tests are included for new features
- License documentation is updated if dependencies change

## License

This application is licensed under the **Apache License 2.0**.

### Dependency Licensing

- **Frappe Framework**: MIT License (used as library)
- **ERPNext**: GPL-3.0 (separate service, API integration only)
- **Frappe Health**: GPL-3.0 (separate service, API integration only)
- **Frappe Drive**: AGPL-3.0 (separate service, API integration only)

For detailed licensing information, see [DEPENDENCIES.md](./DEPENDENCIES.md).

## Support

- GitHub Issues: [https://github.com/opensoft/frappe-app-dartwing/issues](https://github.com/opensoft/frappe-app-dartwing/issues)
- Documentation: See [DEPENDENCIES.md](./DEPENDENCIES.md) for licensing details
