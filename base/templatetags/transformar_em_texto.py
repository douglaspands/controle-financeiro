from django import template
from django.db.models import QuerySet
from typing import Optional

register = template.Library()


@register.filter(is_safe=True)
def queryset_para_texto(queryset: QuerySet, limite: Optional[int] = None) -> str:
    if hasattr(queryset, 'all'):
        qs = queryset.all()
    elif hasattr(queryset, 'objects'):
        qs = queryset.objects.all()
    else:
        return ''
    resultado = ', '.join([str(obj) for obj in qs])
    if limite:
        resultado = resultado[:limite]
    return resultado
