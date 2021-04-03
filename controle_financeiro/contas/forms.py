from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Usuario


class UsuarioAtualizarAdminForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario


class UsuarioCriarAdminForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario


class UsuarioRegistroForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        label=_('Usuário'),
        required=True,
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label=_('Senha'),
        required=True,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label=_('Confirme a senha'),
        required=True,
    )

    first_name = forms.CharField(
        max_length=100,
        label=_('Nome'),
        required=True,
    )

    last_name = forms.CharField(
        max_length=100,
        label=_('Sobrenome'),
        required=True,
    )

    email = forms.EmailField(
        label=_('Email'),
        required=True,
    )

    def clean_username(self):
        if Usuario.objects.filter(username__exact=self.cleaned_data['username']).exists():
            raise forms.ValidationError(_('Já existe um usuário com o mesmo nome.'))
        else:
            return self.cleaned_data['username']

    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise forms.ValidationError(_('Os dois campos de senha não coincidem.'))
        return self.cleaned_data
