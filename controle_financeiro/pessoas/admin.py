from django.contrib import admin
from .models import Pessoa, Fisica, Juridica, Contato, Telefone


admin.site.register(Pessoa)
admin.site.register(Fisica)
admin.site.register(Juridica)
admin.site.register(Contato)
admin.site.register(Telefone)
