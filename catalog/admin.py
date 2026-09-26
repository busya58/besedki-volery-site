from django.contrib import admin

from .models import (
    ConsultationRequest,
    Product,
    ProductRequest,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "product_type",
        "price",
        "old_price",
        "is_featured",
        "is_active",
        "created_at",
    ]

    list_filter = [
        "product_type",
        "is_featured",
        "is_active",
    ]

    search_fields = [
        "title",
        "short_description",
        "description",
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    list_editable = [
        "is_featured",
        "is_active",
    ]


@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "phone",
        "product_type",
        "product",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "product_type",
        "created_at",
    ]

    search_fields = [
        "name",
        "phone",
        "email",
        "comment",
    ]

    list_editable = [
        "status",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "phone",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "created_at",
    ]

    search_fields = [
        "name",
        "phone",
    ]

    list_editable = [
        "status",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]