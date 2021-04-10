from typing import Any, Dict

from base.views import LoginRequiredBase
from carteiras.models import Carteira
from django.views.generic import TemplateView


class IndexView(LoginRequiredBase, TemplateView):
    template_name = 'gerenciamento/index.html'

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["tem_carteira"] = (
            True
            if Carteira.objects.filter(pessoa_id=self.request.user.pessoa.pk).exists()
            else False
        )
        return context
