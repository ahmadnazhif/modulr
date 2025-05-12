# Modulr

Modulr is a modular-based Django project starter designed to simplify the development, installation, upgrade, and removal of independent feature modules — all while supporting dynamic schema and role-based access out of the box.

---

## Features

- **Plug-and-play Modules**  
  Each module is self-contained and can be installed, upgraded, or uninstalled without affecting the rest of the system.

- **Dynamic Schema Sync**  
  Automatically renders the latest model fields into tables/forms based on migration status.

- **Role-Based Access Control**  
  Supports user levels with permission abstraction (using django permission or custom ones).

- **Safe URL Handling**  
  Protect any module endpoint before the module is installed.

- **Scaffold Generator**  
  Command to quickly generate a new compliant module (`./manage.py generate_module {module_name} {module_slug}`).

---

## How the Modular System Works

- Modules are defined as Django apps.
- Each module has:
    - A ModuleConfig with metadata
    - Ways to install, uninstall and upgrade
    - Upgradable module is a module that has unapplied migration
    - A default URL /module-name/ returns empty landing page
    - Optionally other views, models
- Install/uninstall/upgrade logic is abstracted and accessible via UI or admin.

---

## Getting Started

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # follow instruction to create user
python manage.py runserver
```

## Creating New Module
- `./manage.py generate_module {module_name} {module_slug}`
- add `{module_name}` to `INSTALLED_APPS`
- include `{module_name}/urls.py` to `modulr/urls.py`
```bash
path('module/product/', include('product_module.urls'))
```
