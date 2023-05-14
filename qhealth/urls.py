


from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap

from .sitemaps import QHEALTHSitemap

sitemaps = {
    "static": QHEALTHSitemap,
}

urlpatterns = [
    path("", include("frontend.urls", namespace="frontend")),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

handler404 = "frontend.views.handler404"
handler500 = "frontend.views.handler500"

from django.conf import settings
from django.urls import include, path

if settings.DEBUG and False:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
