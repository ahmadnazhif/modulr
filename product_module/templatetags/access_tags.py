from django import template
from ..access_control import PERMISSION_MAP

register = template.Library()

@register.filter
def can(user, permission_name):
    check_func = PERMISSION_MAP.get(permission_name)
    return check_func(user) if check_func else False

@register.filter
def get_attribute(obj, attr):
    return getattr(obj, attr)
