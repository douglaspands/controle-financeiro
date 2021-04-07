from base.views import LoginRequiredBase
from django.views.generic import TemplateView


class IndexView(LoginRequiredBase, TemplateView):
    template_name = 'gerenciamento/index.html'
