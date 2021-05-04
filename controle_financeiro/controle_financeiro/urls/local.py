import debug_toolbar
from django.conf.urls import url
from django.urls import include

from .base import urlpatterns

urlpatterns += [
    url(r"^__debug__/", include(debug_toolbar.urls, namespace="djdt")),
]
