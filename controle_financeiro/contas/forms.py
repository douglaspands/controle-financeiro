from django.contrib.auth import forms
from django.forms import ModelForm

from .models import Usuario


class UsuarioAtualizarAdminForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Usuario


class UsuarioCriarAdminForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Usuario


class UsuarioCriarForm(ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'username': 'Usuario',
            'password': 'Senha',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
        }
