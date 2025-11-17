# frappe-app-dartwing

Frappe framework integration layer for Dartwing with Health, ERPNext, Drive, and multi-service proxy integration.

## Overview

`frappe-app-dartwing` is a custom application layer built on top of the Frappe framework. It provides:

- **Custom business logic** using Frappe's powerful framework
- **Multi-service integration** via proxy/connector patterns for:
  - ERPNext accounting module
  - Frappe Health healthcare management
  - Frappe Drive document management
  - Additional Frappe ecosystem services
- **Clean architectural separation** between custom code and third-party services
- **Apache 2.0 licensing** for the application while respecting dependencies

## Architecture

This application follows a service-oriented architecture with multiple proxy connectors:

```
┌─────────────────────────────────────────┐
│ frappe-app-dartwing Application         │
│ (Apache 2.0 Licensed)                   │
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

## License

This application is licensed under the **Apache License 2.0**.

### Dependency Licensing

This project depends on and integrates with:

- **Frappe Framework**: MIT License
  - Used as a library for application development
  - Custom applications built on Frappe are not restricted by the MIT license

- **ERPNext**: GNU General Public License v3.0 (GPL-3.0)
  - Runs as a separate service
  - This application does NOT include or modify ERPNext code
  - Communication is via REST API/RPC only
  - See [DEPENDENCIES.md](./DEPENDENCIES.md) for detailed licensing information

- **Frappe Health**: GNU General Public License v3.0 (GPL-3.0)
  - Runs as a separate service
  - This application does NOT include or modify Frappe Health code
  - Communication is via REST API/RPC only

- **Frappe Drive**: GNU Affero General Public License v3.0 (AGPL-3.0)
  - Runs as a separate service
  - This application does NOT include or modify Frappe Drive code
  - Communication is via REST API/RPC only

For more details, see the [LICENSE](./LICENSE) file and [DEPENDENCIES.md](./DEPENDENCIES.md).

## Getting Started

### Prerequisites

- Frappe Framework installed and running
- Required services configured and deployed:
  - ERPNext service (for accounting features)
  - Frappe Health service (for healthcare features, optional)
  - Frappe Drive service (for document management, optional)
- Python 3.8+
- Docker (optional, for containerized deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/opensoft/frappe-app-dartwing.git
cd frappe-app-dartwing

# Install dependencies
bench install-app frappe-app-dartwing

# Run migrations
bench migrate
```

### Configuration

Configure service connections in your Frappe site configuration:

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

## Usage

### Multi-Service Proxy Pattern

When users access features through this application:

1. The application receives the request
2. The appropriate service proxy validates and transforms the request
3. The request is forwarded to the service via API
4. The service processes the request
5. Results are returned to the user through this application

### Example: Creating an Accounting Entry

```python
from frappe_app_dartwing.connectors.erpnext_proxy import ERPNextProxy

proxy = ERPNextProxy()
entry_data = {
    'doctype': 'Journal Entry',
    'accounts': [...],
    'posting_date': '2025-12-31'
}
result = proxy.create_document(entry_data)
```

## Development

### Structure

```
frappe-app-dartwing/
├── frappe_app_dartwing/
│   ├── __init__.py
│   ├── hooks.py
│   ├── connectors/
│   │   ├── erpnext_proxy.py       # ERPNext integration
│   │   ├── health_proxy.py         # Frappe Health integration
│   │   ├── drive_proxy.py          # Frappe Drive integration
│   │   └── frappe_helpers.py       # Frappe utilities
│   ├── doctype/
│   │   └── [...custom doctypes]
│   └── api.py                      # REST endpoints
├── tests/
├── LICENSE                         # Apache 2.0
└── README.md
```

### Contributing

Contributions are welcome! Please ensure:

- Code follows the Apache 2.0 license terms
- Service integrations remain as pure proxies (no code modifications)
- Tests are included for new features
- License documentation is updated if dependencies change

## Support

For issues and questions:

- GitHub Issues: [https://github.com/opensoft/frappe-app-dartwing/issues](https://github.com/opensoft/frappe-app-dartwing/issues)
- Documentation: Check [DEPENDENCIES.md](./DEPENDENCIES.md) for licensing details

## License Summary

| Component | License | Notes |
|-----------|---------|-------|
| frappe-app-dartwing | Apache 2.0 | This application |
| Frappe Framework | MIT | Used as library |
| ERPNext | GPL-3.0 | Separate service, API integration only |
| Frappe Health | GPL-3.0 | Separate service, API integration only |
| Frappe Drive | AGPL-3.0 | Separate service, API integration only |

**Note**: For a detailed explanation of the licensing architecture and how service integration works, please see [DEPENDENCIES.md](./DEPENDENCIES.md).
