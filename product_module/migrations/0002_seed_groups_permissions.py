from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups(apps, schema_editor):
    Product = apps.get_model('product_module', 'Product')
    content_type = ContentType.objects.get_for_model(Product)
    manager, _ = Group.objects.get_or_create(name='Manager')
    perms = Permission.objects.filter(content_type=content_type)
    manager.permissions.set(perms)

def remove_permissions(apps, schema_editor):
    Product = apps.get_model('product_module', 'Product')
    content_type = ContentType.objects.get_for_model(Product)

    perms = Permission.objects.filter(content_type=content_type)
    try:
        group = Group.objects.get(name='Manager')
        group.permissions.remove(*perms)
    except Group.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0001_initial'),  # ganti sesuai nama migrasi awal kamu
    ]

    operations = [
        migrations.RunPython(create_groups, remove_permissions),
    ]
