from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .forms import RegistroForm
from .usecases import registrar_usuario_pessoa_fisica


class LogoutConfirmar(TemplateView):
    template_name = "registration/logout_confirmar.html"


class UsuarioCriar(View):
    form_class = RegistroForm
    template_name = "autenticacao/usuario_criar.html"
    context_object_name = "usuario"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            registrar_usuario_pessoa_fisica(form)
            return render(request, "autenticacao/usuario_criar_concluido.html", {})
        else:
            return render(request, self.template_name, {"form": form})
