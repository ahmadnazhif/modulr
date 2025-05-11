from django.contrib.auth.models import User


PERMISSION_MAP = {
    'create_product': lambda user: user and user.is_authenticated,
    'read_product': lambda user: True,
    'update_product': lambda user: user and user.is_authenticated,
    'delete_product': lambda user: user.is_authenticated and user.has_perm('product_module.delete_product'),
}
