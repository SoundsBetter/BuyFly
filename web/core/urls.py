from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from django.conf import settings

from .views import home

API_DOMAIN = settings.API_DOMAIN


urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{API_DOMAIN}/accounts/", include("apps.accounts.api_urls")),
    path(f"{API_DOMAIN}/flights/", include("apps.flights.api_urls")),
    path(f"{API_DOMAIN}/bookings/", include("apps.bookings.api_urls")),
    path(f"{API_DOMAIN}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"{API_DOMAIN}/schema/swagger-ui/",
         SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"{API_DOMAIN}/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("", include("apps.bookings.urls")),
    path("home/", home, name="home")
]
