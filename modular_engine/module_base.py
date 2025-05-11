from abc import ABC, abstractmethod
from django.apps import apps
from django.core.management import call_command
from django.utils import timezone
from modular_engine.models import Module
from modular_engine.utils.safe_factory import get_safe_model, remove_safe_model

class BaseModuleInstaller(ABC):
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
        return Module.objects.get(
            name=self.module_name,
            slug=self.module_slug
        )

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

        if not chosen_module.needs_upgrade:
            return

        call_command("migrate", chosen_module.name)

        all_models = apps.get_app_config(chosen_module.name).get_models()

        for model in all_models:
            remove_safe_model(model)

        current_time = timezone.now()
        chosen_module.upgraded_at = current_time
        chosen_module.save()
