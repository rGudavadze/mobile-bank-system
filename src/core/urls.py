from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin Site URLs
    path("admin/", admin.site.urls),
    # User Related URLs
    path("api/", include("apps.users.urls")),
    # API Schema URLs
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/", include("apps.cards.urls")),
]
