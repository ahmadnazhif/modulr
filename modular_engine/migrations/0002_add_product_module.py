from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_module(apps, schema_editor):
    Module = apps.get_model('modular_engine', 'Module')
    Module.objects.get_or_create(
        name='product_module',
        slug='product',
    )

def remove_module(apps, schema_editor):
    Module = apps.get_model('modular_engine', 'Module')
    Module.objects.filter(
        name='product_module',
        slug='product',
    ).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('modular_engine', '0001_initial'),  # ganti sesuai nama migrasi awal kamu
    ]

    operations = [
        migrations.RunPython(create_module, remove_module),
    ]
