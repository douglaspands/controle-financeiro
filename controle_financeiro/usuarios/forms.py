from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Usuario


class UsuarioAtualizarAdminForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario


class UsuarioCriarAdminForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
