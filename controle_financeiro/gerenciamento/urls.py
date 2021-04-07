from django.urls import path
from .views import IndexView

app_name = "gerenciamento"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
