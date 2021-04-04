from django.contrib import admin
from .models import Categoria, Lancamento


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'atualizado_em')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'atualizado_em'


admin.site.register(Lancamento)
