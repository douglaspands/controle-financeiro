from django.contrib import admin

from .models import Categoria, Despesa, Lancamento, Parcela, Receita


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "slug", "atualizado_em")
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = "atualizado_em"


admin.site.register(Lancamento)
admin.site.register(Receita)
admin.site.register(Despesa)
admin.site.register(Parcela)
