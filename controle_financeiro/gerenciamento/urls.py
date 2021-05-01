from django.urls import path
from .views import TemplateExampleView, RedirectView

app_name = "gerenciamento"

urlpatterns = [
    path("", RedirectView.as_view(), name="index"),
    path("template", TemplateExampleView.as_view(), name="example"),
]
