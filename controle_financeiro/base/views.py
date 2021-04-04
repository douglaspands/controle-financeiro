from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LoginRequiredBase(LoginRequiredMixin):
    login_url = reverse_lazy('autenticacao:login')
    redirect_field_name = 'redirect_to'
