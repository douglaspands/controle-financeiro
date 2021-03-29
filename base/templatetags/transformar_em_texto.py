from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter(is_safe=True)
def queryset_para_texto(queryset: QuerySet) -> str:
    return ', '.join([str(obj) for obj in queryset.all()])
