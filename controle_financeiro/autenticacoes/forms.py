import re

from django import forms
from django.utils.translation import gettext_lazy as _
from usuarios.models import Usuario


class RegistroForm(forms.Form):

    REGEX_USERNAME = r'^[a-zA-Z0-9]([._-](?![._-])|[a-zA-Z0-9]){3,18}[a-zA-Z0-9]$'

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
        if not re.search(self.REGEX_USERNAME, self.cleaned_data['username']):
            raise forms.ValidationError(
                _('Favor use somente letras, números e períodos.')
            )
        if Usuario.objects.filter(
            username__exact=self.cleaned_data['username']
        ).exists():
            raise forms.ValidationError(_('Já existe um usuário com o mesmo nome.'))
        else:
            return self.cleaned_data['username']

    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise forms.ValidationError(_('Os dois campos de senha não coincidem.'))
        return self.cleaned_data
