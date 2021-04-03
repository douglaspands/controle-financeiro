from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.hashers import make_password

from .forms import UsuarioCriarForm
from .models import Usuario


class LogoutConfirmar(TemplateView):
    template_name = "registration/logout_confirmar.html"


class LogoutConcluido(TemplateView):
    template_name = "registration/logout_concluido.html"


class UsuarioCriar(CreateView):
    model = Usuario
    form_class = UsuarioCriarForm
    template_name = "contas/usuario_criar.html"
    context_object_name = "usuario"

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UsuarioCriarForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(usuario.password)
            usuario.save()
            grupo = Group.objects.get(id=1)
            grupo.user_set.add(usuario)
            grupo.save()
            return render(request, 'contas/usuario_criar_concluido.html', {})
        else:
            return render(request, self.template_name, {'form': form})
