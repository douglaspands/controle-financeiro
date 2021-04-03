from django.contrib import admin

from .models import Carteira, Tipo


@admin.register(Tipo)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'permite_parcelamento')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'atualizado_em'


admin.site.register(Carteira)
