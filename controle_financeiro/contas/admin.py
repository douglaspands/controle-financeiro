from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UsuarioAtualizarForm, UsuarioCriarForm
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(auth_admin.UserAdmin):
    form = UsuarioAtualizarForm
    add_form = UsuarioCriarForm
    model = Usuario
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        (_('Cadastro Extra'), {'fields': ('perfil',)}),
        (_('Informações Pessoais Extra'), {'fields': ('data_nascimento',)}),
    )
