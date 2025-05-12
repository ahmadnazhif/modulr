from django.conf import settings
from importlib.util import find_spec

from django.db import connections, DEFAULT_DB_ALIAS
from django.db.migrations.loader import MigrationLoader

def discover_modules():
    modules = []
    for app in settings.INSTALLED_APPS:
        if find_spec(f"{app}.install"):
            modules.append(app)
    return modules


def app_has_unapplied_migrations(app_label: str) -> bool:
    connection = connections[DEFAULT_DB_ALIAS]
    loader = MigrationLoader(connection, ignore_no_migrations=True)
    graph = loader.graph

    # Get applied and all known migrations
    applied = set(loader.applied_migrations.keys())
    all_for_app = {
        key for key in graph.nodes.keys() if key[0] == app_label
    }

    # Check if any are not applied
    unapplied = all_for_app - applied
    return bool(unapplied)
