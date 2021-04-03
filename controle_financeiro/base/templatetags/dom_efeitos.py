from django import template
from django.http import HttpRequest

register = template.Library()


@register.filter(is_safe=True)
def nav_item_active(request: HttpRequest, apps_names: str) -> str:
    _apps_names = apps_names.split(',')
    _namespace = request.path.split('/')[1]
    if _namespace in _apps_names:
        return ' active'
    else:
        return ''


@register.filter()
def span_sr_only(request: HttpRequest, apps_names: str) -> bool:
    _apps_names = apps_names.split(',')
    _namespace = request.path.split('/')[1]
    if _namespace in _apps_names:
        return True
    else:
        return False
