from django.contrib.auth import forms

from .models import Usuario


class UsuarioAtualizarForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Usuario


class UsuarioCriarForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Usuario
