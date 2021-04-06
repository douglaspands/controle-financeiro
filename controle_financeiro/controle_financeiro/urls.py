"""controle_financeiro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.publico, name='publico')
Class-based views
    1. Add an import:  from other_app.views import Publico
    2. Add a URL to urlpatterns:  path('', Publico.as_view(), name='publico')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('publico.urls', namespace='publico')),
    path('admin/', admin.site.urls),
    path('gerenciamento/', include('gerenciamento.urls', namespace='gerenciamento')),
]

if settings.SETTING_NAME in ['local', 'test']:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls, namespace='djdt')),
    ]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
