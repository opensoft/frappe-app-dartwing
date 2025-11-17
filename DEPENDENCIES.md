# Dependencies and Licensing

This document explains the licensing architecture of `frappe-app-dartwing` and how it manages dependencies while maintaining Apache 2.0 licensing through multiple service proxies.

## Overview

`frappe-app-dartwing` is licensed under **Apache License 2.0** and integrates with multiple Frappe ecosystem components:

1. **Frappe Framework** (MIT License) - Used as a core library
2. **ERPNext** (GPL-3.0 License) - Accessed via API as a separate service
3. **Frappe Health** (GPL-3.0 License) - Accessed via API as a separate service
4. **Frappe Drive** (AGPL-3.0 License) - Accessed via API as a separate service

This document explains how we maintain Apache 2.0 licensing while respecting the licenses of all dependencies.

## License Compatibility Matrix

| Component | License | Integration Type | Code Inclusion | License Impact |
|-----------|---------|------------------|-----------------|----------------|
| frappe-app-dartwing | Apache 2.0 | N/A | This repo | Primary license |
| Frappe Framework | MIT | Library import | No | MIT is compatible with Apache 2.0 |
| ERPNext | GPL-3.0 | HTTP/RPC API | No | No GPL contamination |
| Frappe Health | GPL-3.0 | HTTP/RPC API | No | No GPL contamination |
| Frappe Drive | AGPL-3.0 | HTTP/RPC API | No | No AGPL contamination |

## Frappe Framework (MIT License)

### License Details

The Frappe Framework is licensed under the MIT License. MIT is a permissive open source license that:

- Allows commercial use
- Allows modification
- Allows distribution
- Allows private use
- Requires License and Copyright Notice
- Provides no warranty or liability

**MIT License Text**: https://github.com/frappe/frappe/blob/develop/LICENSE

### Why Apache 2.0 Works with MIT

Our application can be licensed under Apache 2.0 when using the Frappe Framework because:

1. **MIT is permissive**: MIT allows code to be used in projects with different licenses
2. **No GPL requirements**: MIT does not impose copyleft requirements (unlike GPL)
3. **Apache 2.0 is compatible**: Apache 2.0 is also a permissive license
4. **Library usage**: We use Frappe as a library, not as derivative work

### How We Use Frappe

- Import Frappe Framework as a Python package
- Build custom applications on top of Frappe
- Do NOT modify Frappe framework source code
- Do NOT redistribute Frappe code

**Result**: Custom applications built on Frappe are not restricted by MIT license terms

## ERPNext (GPL-3.0 License)

### License Details

ERPNext is licensed under the GNU General Public License v3.0 (GPL-3.0). GPL-3.0 is a **copyleft** license that:

- Allows commercial use
- Allows modification
- Allows distribution
- Requires source code disclosure
- Requires derivative works to use the same GPL-3.0 license (copyleft)
- Requires License and Copyright Notice
- Provides no warranty or liability

**GPL-3.0 License Text**: https://www.gnu.org/licenses/gpl-3.0.html

### Why GPL-3.0 Does NOT Affect Our License

Our application remains Apache 2.0 licensed because:

1. **No code embedding**: We do NOT include, modify, or redistribute ERPNext source code
2. **API-only integration**: All communication with ERPNext happens via REST API/RPC calls
3. **Separate deployment**: ERPNext runs as an independent service with its own GPL-3.0 licensing
4. **No derivative work**: We do not create derivative works of ERPNext code
5. **Proxy pattern**: We act as a client/proxy to ERPNext, not as a modification of it

### Architectural Separation

```
frappe-app-dartwing (Apache 2.0)
↓ (HTTP/RPC API calls)
ERPNext Service (GPL-3.0)
```

The separation is:

- **Network boundary**: ERPNext is accessed over HTTP/RPC
- **Process boundary**: ERPNext runs in separate process(es)
- **Code boundary**: No ERPNext source code is included in this repository
- **License boundary**: GPL-3.0 terms apply to ERPNext deployment only

### GPL-3.0 and Service Usage

GPL-3.0 is primarily concerned with:

- Modifying GPL-licensed software
- Redistributing GPL-licensed software
- Creating derivative works from GPL-licensed software

GPL-3.0 is **NOT** concerned with:

- Using GPL-licensed software as a service
- Communicating with GPL-licensed software via APIs
- Building applications that call into GPL-licensed services

**Reference**: https://www.gnu.org/licenses/gpl-faq.html#AGPLProxy

## Frappe Health (GPL-3.0 License)

### Overview

Frappe Health is a healthcare management module licensed under GPL-3.0. Like ERPNext:

- **Runs as separate service**: Independent deployment
- **API-based access**: No code embedding
- **No license contamination**: GPL-3.0 applies to Health module only

### Integration Pattern

```
frappe-app-dartwing (Apache 2.0)
↓ (HTTP/RPC API calls)
Frappe Health Service (GPL-3.0)
```

- Accessed exclusively via REST/RPC APIs
- No Frappe Health source code in this repository
- GPL-3.0 terms apply only to Health module deployment

**Repository**: https://github.com/frappe/health

## Frappe Drive (AGPL-3.0 License)

### Overview

Frappe Drive is a document management module licensed under AGPL-3.0. AGPL-3.0 is similar to GPL-3.0 with an additional network provision:

- **Stricter than GPL-3.0**: Includes "network use" clause
- **Separate deployment**: Runs as independent service
- **API-based access**: No code embedding

### Integration Pattern

```
frappe-app-dartwing (Apache 2.0)
↓ (HTTP/RPC API calls)
Frappe Drive Service (AGPL-3.0)
```

- Accessed exclusively via REST/RPC APIs
- No Frappe Drive source code in this repository
- AGPL-3.0 terms apply only to Drive module deployment

**Repository**: https://github.com/frappe/drive

## Multi-Service Proxy Architecture

The application uses a **modular proxy pattern** for each service:

```
┌─────────────────────────────────┐
│ frappe-app-dartwing             │
│ (Apache 2.0 Licensed)            │
├─────────────────────────────────┤
│ Service-specific proxy connectors:
│ - erpnext_proxy.py
│ - health_proxy.py
│ - drive_proxy.py
│ - frappe_helpers.py
└─────────────────────────────────┘
        ↓ (HTTP/RPC APIs)
┌─────────────────────────────────┐
│ External Services (Independent  │
│ Deployments)                    │
├─────────────────────────────────┤
│ - ERPNext (GPL-3.0)             │
│ - Frappe Health (GPL-3.0)       │
│ - Frappe Drive (AGPL-3.0)       │
│ - Frappe Framework (MIT)        │
└─────────────────────────────────┘
```

### Key Principles

1. **Proxy Pattern**: Each service has its own proxy/connector
2. **No Code Embedding**: Services remain external
3. **API Communication**: Only HTTP/RPC messages exchanged
4. **License Isolation**: Each service's license applies only to that service
5. **Clean Boundaries**: Clear separation between application and services

## Detailed Licensing Breakdown

### frappe-app-dartwing Application Code

**License**: Apache License 2.0

**What's Included**:
- Custom business logic
- Frappe integration layer
- Multi-service proxy/connector classes
- REST API endpoints
- Database models (DocTypes)
- Custom views and templates
- Tests and documentation

**License File**: LICENSE

### Frappe Framework

**License**: MIT License

**Installation**: `pip install frappe` (external dependency)

**Included in Repo**: No (installed as external package)

**Usage**:
- Imported as Python package
- Used through Frappe's public API
- NOT modified or redistributed

**License Acknowledgment**: Include Frappe's MIT license notice in documentation

**See**: https://github.com/frappe/frappe/blob/develop/LICENSE

### ERPNext Service

**License**: GNU General Public License v3.0

**Installation**: Deployed as separate service (not in this repository)

**Included in Repo**: No (accessed via API only)

**Usage**:
- Accessed via REST API/RPC
- No source code included
- No source code modified
- No source code redistributed

**License Acknowledgment**: Deploy ERPNext under GPL-3.0 terms

**See**: https://github.com/frappe/erpnext/blob/develop/LICENSE

### Frappe Health Service

**License**: GNU General Public License v3.0

**Installation**: Deployed as separate service

**Included in Repo**: No (accessed via API only)

**Usage**: Same as ERPNext - accessed via REST/RPC APIs only

### Frappe Drive Service

**License**: GNU Affero General Public License v3.0

**Installation**: Deployed as separate service

**Included in Repo**: No (accessed via API only)

**Usage**: Same as ERPNext - accessed via REST/RPC APIs only

## User Obligations

### For frappe-app-dartwing Code

✅ You must:
- Provide license notice (Apache 2.0)
- Include copy of Apache 2.0 license
- State significant changes made

❌ You cannot:
- Remove Apache 2.0 license notice
- Hold maintainers liable
- Claim trademark rights

### For Frappe Framework

✅ You must:
- Include Frappe's MIT license notice
- Include copy of MIT license

### For ERPNext, Frappe Health, Frappe Drive

✅ When deploying these services:
- Follow their respective licenses
- Provide source code if you modify them
- Include proper license notices

❌ You cannot:
- Use their code outside their license terms
- Remove license notices

## FAQ

### Q: Can I use this under a different license?

A: No. This application is licensed under Apache 2.0.

### Q: Do I need to open-source my code if I use this?

A: **No**. Apache 2.0 is a permissive license that does not require you to open-source your code. You must include the license notice and copyright attribution.

### Q: What if I modify a service like ERPNext?

A: If you modify ERPNext:
- Your modifications fall under GPL-3.0
- You must provide source code for modifications
- The `frappe-app-dartwing` application itself remains Apache 2.0

### Q: How do I properly attribute licenses?

A: Include in your project:
- Copy of Apache 2.0 license (this app)
- Copy of MIT license (Frappe)
- Copies of respective licenses for deployed services

Example:
```
Licenses:
- frappe-app-dartwing: Apache License 2.0
- Frappe Framework: MIT License
- ERPNext: GNU General Public License v3.0
- Frappe Health: GNU General Public License v3.0
- Frappe Drive: GNU Affero General Public License v3.0
```

## References

### Licenses

- Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0
- MIT License: https://opensource.org/licenses/MIT
- GPL-3.0 License: https://www.gnu.org/licenses/gpl-3.0.html
- AGPL-3.0 License: https://www.gnu.org/licenses/agpl-3.0.html

### Documentation

- Frappe Framework: https://github.com/frappe/frappe
- ERPNext: https://github.com/frappe/erpnext
- Frappe Health: https://github.com/frappe/health
- Frappe Drive: https://github.com/frappe/drive
- GPL and Services: https://www.gnu.org/licenses/gpl-faq.html

### Related

- README.md - Main documentation
- LICENSE - Apache 2.0 license text

**Last Updated**: November 2025
