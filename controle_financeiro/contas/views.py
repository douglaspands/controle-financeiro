from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .forms import UsuarioRegistroForm
from .models import Usuario


class LogoutConfirmar(TemplateView):
    template_name = "registration/logout_confirmar.html"


class UsuarioCriar(View):
    form_class = UsuarioRegistroForm
    template_name = "contas/usuario_criar.html"
    context_object_name = "usuario"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            usuario = Usuario(
                username=form.cleaned_data['username'],
                password=make_password(form.cleaned_data['password1']),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
            )
            usuario.save()
            grupo = Group.objects.get(id=1)
            grupo.user_set.add(usuario)
            grupo.save()
            return render(request, 'contas/usuario_criar_concluido.html', {})
        else:
            return render(request, self.template_name, {'form': form})
