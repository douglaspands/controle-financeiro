from django.contrib import admin
from .models import Tipo


@admin.register(Tipo)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'permite_parcelamento')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'atualizado_em'
