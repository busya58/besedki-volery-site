from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from pages.robots import robots_txt
from pages.seo_views import seo_page
from pages.sitemaps import (
    MainSitemap,
    ProductSitemap,
    SeoPageSitemap,
)


sitemaps = {
    "main": MainSitemap,
    "products": ProductSitemap,
    "seo": SeoPageSitemap,
}


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": sitemaps,
        },
        name="sitemap",
    ),

    path(
        "robots.txt",
        robots_txt,
        name="robots_txt",
    ),

    path(
        "",
        include("catalog.urls"),
    ),

    # SEO-страницы беседок
    path(
        "besedki/<slug:slug>/",
        seo_page,
        {
            "category": "gazebo",
        },
        name="seo_gazebo",
    ),

    # SEO-страницы вольеров
    path(
        "volery/<slug:slug>/",
        seo_page,
        {
            "category": "enclosure",
        },
        name="seo_enclosure",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
