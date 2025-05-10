from django.conf import settings
from importlib.util import find_spec

def discover_modules():
    # TODO create script to create new module and necessary files
    modules = []
    for app in settings.INSTALLED_APPS:
        if find_spec(f"{app}.install"):
            modules.append(app)
    return modules
