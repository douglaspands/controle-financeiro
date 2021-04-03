# from django.shortcuts import render
from django.views.generic import TemplateView


class LogoutConfirmarView(TemplateView):
    template_name = 'registration/logout_confirmar.html'


class LogoutConcluidoView(TemplateView):
    template_name = 'registration/logout_concluido.html'
