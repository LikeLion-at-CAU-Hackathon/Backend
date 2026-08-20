from django.contrib import admin
from .models import *


# admin.site.register(Product)
admin.site.register(ProductDetail)
# admin.site.register(ProductImage)
admin.site.register(Branch)
admin.site.register(Stock)
admin.site.register(BusinessHours)

admin.site.register(Material)
admin.site.register(MaterialProduct)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
    )

    search_fields = (
        "=id",
        "name",
    )

    list_filter = (
        "category",
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_product_id",
        "get_product",
        "get_size",
        "get_color",
        "image",
        "order",
    )

    search_fields = (
        "=detail__product__id",
        "detail__product__name",
        "detail__size",
        "detail__color",
    )

    list_filter = (
        "detail__product",
        "detail__size",
        "detail__color",
    )

    def get_product_id(self, obj):
        return obj.detail.product.id
    get_product_id.short_description = "Product ID"

    def get_product(self, obj):
        return obj.detail.product.name
    get_product.short_description = "Product"

    def get_size(self, obj):
        return obj.detail.size
    get_size.short_description = "Size"

    def get_color(self, obj):
        return obj.detail.color
    get_color.short_description = "Color"