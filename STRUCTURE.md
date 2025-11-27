# Dartwing App Structure

This document describes the folder structure of the Dartwing Frappe app, following standard Frappe framework conventions.

## Root Directory

```
frappe-app-dartwing/          # Repository root
├── .git/                     # Git repository
├── .gitignore               # Git ignore rules
├── API.md                   # API documentation
├── DEPENDENCIES.md          # Dependency licensing information
├── LICENSE                  # Apache 2.0 license
├── README.md                # Project overview
├── STRUCTURE.md             # This file - folder structure documentation
├── pyproject.toml           # Python package configuration
└── dartwing/                # Main Python package (the app itself)
```

## Main Package Structure (`dartwing/`)

```
dartwing/
├── __init__.py              # Package initialization
├── hooks.py                 # Frappe framework hooks and app configuration
├── modules.txt              # List of modules in the app
├── patches.txt              # Database migration patches
│
├── api/                     # REST API endpoints
│   ├── __init__.py
│   └── family.py            # Family management API
│
├── config/                  # App configuration
│   └── __init__.py
│
├── doctype/                 # Frappe DocTypes (database models)
│   ├── __init__.py
│   └── family/              # Family DocType
│       ├── __init__.py
│       ├── family.json      # DocType definition (schema)
│       └── family.py        # DocType controller (business logic)
│
├── fixtures/                # Data import/export files
│   └── .gitkeep
│
├── public/                  # Public web assets
│   ├── css/                 # Stylesheets
│   │   └── .gitkeep
│   └── js/                  # JavaScript files
│       └── .gitkeep
│
├── templates/               # HTML templates (Jinja2)
│   └── .gitkeep
│
├── tests/                   # Automated test scripts
│   └── .gitkeep
│
└── www/                     # Static web pages (served directly)
    └── .gitkeep
```

## Directory Descriptions

### Core Files

- **`__init__.py`**: Makes the directory a Python package. Contains package-level initialization code.
- **`hooks.py`**: Defines how the app integrates with Frappe framework. Contains app metadata, event hooks, scheduled tasks, permissions, etc.
- **`modules.txt`**: Lists all modules available in the app. Currently contains "Dartwing" module.
- **`patches.txt`**: Database migration scripts executed in order during `bench migrate`.

### Application Directories

#### `api/`
Contains REST API endpoints exposed via Frappe's whitelisted methods. These are accessible at `/api/method/dartwing.api.<module>.<function>`.

**Current files:**
- `family.py`: Family/Organization management CRUD API

**Usage:** Add new API modules here as separate Python files.

#### `config/`
Configuration files for the app, including:
- Desktop icons
- Module definitions
- App-specific settings

**Currently:** Empty (standard __init__.py only)

#### `doctype/`
Contains Frappe DocType definitions. Each DocType represents a database table/model.

**Structure per DocType:**
```
doctype/
└── <doctype_name>/
    ├── __init__.py
    ├── <doctype_name>.json    # Schema definition (fields, permissions)
    ├── <doctype_name>.py      # Controller (validation, business logic)
    ├── <doctype_name>.js      # Client-side behavior (optional)
    └── test_<doctype_name>.py # Unit tests (optional)
```

**Current DocTypes:**
- `family/`: Family/Organization management

**Usage:** Add new DocTypes via `bench new-doctype` command.

#### `fixtures/`
Data fixtures for exporting/importing standard data:
- Default records
- Configuration data
- Master data

**Format:** JSON files that can be exported/imported via `bench export-fixtures` and `bench import-fixtures`.

**Currently:** Empty

#### `public/`
Publicly accessible static assets served by the web server.

**Subdirectories:**
- `css/`: Stylesheets for customizing UI
- `js/`: JavaScript files for client-side functionality
- `images/`: Images and icons (add as needed)
- `build/`: Compiled/bundled assets (auto-generated)

**URL Mapping:** Files here are accessible at `/assets/dartwing/<path>`

**Currently:** Empty (ready for assets)

#### `templates/`
Jinja2 HTML templates for:
- Custom web pages
- Email templates
- Print formats
- Reports

**Subdirectories (add as needed):**
- `pages/`: Web page templates
- `emails/`: Email templates
- `print_formats/`: Printable document templates

**Currently:** Empty

#### `tests/`
Automated test scripts using Frappe's test framework (unittest-based).

**Naming convention:** `test_<module>.py`

**Usage:**
```bash
# Run all tests
bench --site <site> run-tests --app dartwing

# Run specific test
bench --site <site> run-tests dartwing.tests.test_family
```

**Currently:** Empty (tests to be added)

#### `www/`
Static web pages served directly without routing through Frappe's page system.

**Features:**
- Files with `.html`, `.md` extensions served directly
- Supports Jinja2 templating
- Auto-routing: `www/about.html` → `/about`
- Can include Python files: `www/page.py` + `www/page.html`

**Currently:** Empty

## Adding New Components

### Add a new DocType
```bash
bench --site <site> new-doctype "Member"
```
This creates: `dartwing/doctype/member/`

### Add a new API module
Create: `dartwing/api/member.py`
```python
import frappe

@frappe.whitelist()
def get_members():
    return frappe.get_all("Member")
```

### Add a static page
Create: `dartwing/www/about.html`
```html
<h1>About Dartwing</h1>
<p>Family management system</p>
```
Accessible at: `/about`

### Add client-side script
Create: `dartwing/public/js/dartwing.js`

Reference in `hooks.py`:
```python
app_include_js = "/assets/dartwing/js/dartwing.js"
```

### Add fixtures
Export current data:
```bash
bench --site <site> export-fixtures
```

Import fixtures:
```bash
bench --site <site> import-fixtures
```

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| DocType | snake_case | `family.py` |
| API Module | snake_case | `family.py` |
| Test File | test_<name>.py | `test_family.py` |
| Python Class | PascalCase | `class Family(Document)` |
| JS File | lowercase | `dartwing.js` |
| Template | lowercase.html | `family_list.html` |

## Best Practices

1. **Separation of Concerns**: Keep API logic in `api/`, business logic in DocType controllers
2. **Testing**: Add tests for all new features in `tests/`
3. **Documentation**: Update API.md when adding new endpoints
4. **Assets**: Organize CSS/JS files logically in `public/`
5. **Fixtures**: Use fixtures for standard/default data
6. **Patches**: Use patches for database schema changes

## Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Add code** (DocType, API, etc.)
   
3. **Run migrations**
   ```bash
   bench --site <site> migrate
   ```

4. **Test**
   ```bash
   bench --site <site> run-tests --app dartwing
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

## Resources

- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [Frappe App Development Tutorial](https://frappeframework.com/docs/user/en/tutorial)
- [API Documentation](./API.md)
- [Dependencies](./DEPENDENCIES.md)

## License

Apache 2.0 - See [LICENSE](./LICENSE)
