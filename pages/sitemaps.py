from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from catalog.models import Product
from .seo_data import SEO_PAGES


class MainSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            "home",
            "catalog_gazebo",
            "catalog_aviary",
        ]

    def location(self, item):
        if item == "home":
            return reverse("home")

        if item == "catalog_gazebo":
            return reverse(
                "catalog",
                kwargs={"product_type": "gazebo"},
            )

        if item == "catalog_aviary":
            return reverse(
                "catalog",
                kwargs={"product_type": "aviary"},
            )

        return "/"


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(
            is_active=True
        ).order_by("pk")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class SeoPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return list(SEO_PAGES.keys())

    def location(self, item):
        category, slug = item

        if category == "gazebo":
            return reverse(
                "seo_gazebo",
                kwargs={"slug": slug},
            )

        if category == "enclosure":
            return reverse(
                "seo_enclosure",
                kwargs={"slug": slug},
            )

        return "/"
