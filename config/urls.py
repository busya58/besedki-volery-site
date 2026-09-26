from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from pages.seo_views import seo_page


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("catalog.urls")),

    # SEO-страницы беседок
    path(
        "besedki/<slug:slug>/",
        seo_page,
        {"category": "gazebo"},
        name="seo_gazebo",
    ),

    # SEO-страницы вольеров
    path(
        "volery/<slug:slug>/",
        seo_page,
        {"category": "enclosure"},
        name="seo_enclosure",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )