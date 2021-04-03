from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import UsuarioAtualizarAdminForm, UsuarioCriarAdminForm
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(auth_admin.UserAdmin):
    form = UsuarioAtualizarAdminForm
    add_form = UsuarioCriarAdminForm
    model = Usuario
