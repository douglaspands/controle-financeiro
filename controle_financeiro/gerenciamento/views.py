from typing import Any, Dict

from base.views import LoginRequiredBase
from carteiras.models import Carteira
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, View


class TemplateExampleView(LoginRequiredBase, TemplateView):
    template_name = "gerenciamento/index.html"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["tem_carteira"] = (
            True
            if Carteira.objects.filter(usuario_id=self.request.user.pk).exists()
            else False
        )
        return context


class RedirectView(LoginRequiredBase, View):
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:

        carteiras = Carteira.objects.filter(usuario=request.user)

        if carteiras.exists():
            carteira_principal = carteiras.filter(principal=True).first()
            if not carteira_principal:
                carteira_principal = carteiras.first()
                carteira_principal.principal = True
                carteira_principal.save()
            return redirect(
                "carteiras:detalhar", slug=carteira_principal.slug
            )
        else:
            return redirect("carteiras:criar")
