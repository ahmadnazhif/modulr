from abc import ABC, abstractmethod
from datetime import timezone
from django.core.management import call_command

from modular_engine.models import Module

class BaseModuleInstaller:
    @property
    @abstractmethod
    def module_name(self):
        """Name of the module to be installed."""
        pass

    @property
    @abstractmethod
    def module_slug(self):
        """Slug of the module to be installed."""
        pass

    def _get_module(self) -> Module:
        return Module.objects.get_or_create(
            name=self.module_name,
            defaults={
                "slug":  self.module_slug,
            }
        )[0]

    def install(self):
        chosen_module = self._get_module()
        if chosen_module.is_installed:
            return

        call_command("migrate", chosen_module.name)
        current_time = timezone.now()
        chosen_module.is_installed = True
        chosen_module.installed_at = chosen_module.upgraded_at = current_time
        chosen_module.save()

    def uninstall(self):
        chosen_module = self._get_module()
        if not chosen_module.is_installed:
            return

        chosen_module.is_installed = False
        chosen_module.save()

    def upgrade(self):
        chosen_module = self._get_module()
        if not chosen_module.is_installed:
            return

        call_command("migrate", chosen_module.name)
        current_time = timezone.now()
        chosen_module.upgraded_at = current_time
        chosen_module.save()
