from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import debug_toolbar

urlpatterns = [
    path("", include("rpna.alerts.urls", namespace="alerts")),
    path("api/", include("rpna.api.urls")),
    path("admin/", admin.site.urls),
    path("grappelli/", include("grappelli.urls")),
]

if settings.ALLOW_DEBUG:
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
