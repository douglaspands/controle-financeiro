from django.urls import include, path

app_name = 'gerenciamento'

urlpatterns = [
    # path('', include('publico.urls', namespace='publico')),
    path('carteiras/', include('carteiras.urls', namespace='carteiras')),
]
