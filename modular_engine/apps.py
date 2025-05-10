from django.apps import AppConfig


class ModularEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modular_engine'

    def ready(self):
        from django.db.utils import OperationalError
        from modular_engine.models import Module
        from modular_engine.utils.discover import discover_modules

        try:
            discovered = discover_modules()
            for mod_name in discovered:
                Module.objects.get_or_create(name=mod_name)
        except OperationalError:
            # Skip if DB not ready (e.g., during `migrate`)
            pass
