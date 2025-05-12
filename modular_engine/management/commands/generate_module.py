import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import subprocess

from modular_engine.models import Module


INSTALLER_TEMPLATE = """
from modular_engine.module_base import BaseModuleInstaller

class {class_name}Installer(BaseModuleInstaller):
    module_name = "{module_name}"
    module_slug = "{module_slug}"

installer = {class_name}Installer()
"""

URL_TEMPLATE = """
from django.urls import path
from django.shortcuts import render

urlpatterns = [
    path('', lambda request: render(request, 'modular_engine/coming_soon.html'), name='{module_slug}_landing_page'),
]
"""


class Command(BaseCommand):
    help = "Generate a new modular app with required boilerplate"

    def add_arguments(self, parser):
        parser.add_argument('module_name', type=str, help='The name of the new module (usually with _module postfix)')
        parser.add_argument('module_slug', type=str, help='Slug of the module')

    def handle(self, *args, **options):
        module_name: str = options['module_name']
        module_slug: str = options['module_slug']
        project_dir = settings.BASE_DIR
        module_path = os.path.join(project_dir, module_name)

        if os.path.exists(module_path):
            raise CommandError(f"Module {module_name} already exists.")
        
        if Module.objects.filter(slug=module_slug).exists():
            raise CommandError(f"Module with slug {module_slug} already exists.")

        subprocess.call(['python', 'manage.py', 'startapp', module_name])

        # Add install.py
        with open(os.path.join(module_path, 'install.py'), 'w') as f:
            f.write(INSTALLER_TEMPLATE.format(
                class_name=module_name.capitalize(),
                module_name=module_name,
                module_slug=module_slug.lower()
            ))
        
        # Add urls.py
        with open(os.path.join(module_path, 'urls.py'), 'w') as f:
            f.write(URL_TEMPLATE.format(
                module_slug=module_slug.lower()
            ))

        Module.objects.create(
            name=module_name,
            slug=module_slug
        )
        self.stdout.write(self.style.SUCCESS(f"Modular app '{module_name}' created successfully."))
