from django import template

register = template.Library()


@register.filter(is_safe=True)
def nav_item_active(view, app_name: str) -> str:
    if view.template_name.split('/')[0] == app_name:
        return ' active'
    else:
        return ''


@register.filter()
def span_sr_only(view, app_name: str) -> bool:
    if view.template_name.split('/')[0] == app_name:
        return True
    else:
        return False
