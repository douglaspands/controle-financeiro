from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name='home/index.html'
