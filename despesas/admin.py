from django.contrib import admin
from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'atualizado_em')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'atualizado_em'
