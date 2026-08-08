from django.contrib import admin
from .models import (
    ProductGroup,
    Product,
    Collection,
    ProductDetail,
    Stock,
    ProductImage,
    NFCTag,
    Branch,
)

admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(Collection)
admin.site.register(ProductDetail)
admin.site.register(Stock)
admin.site.register(ProductImage)
admin.site.register(NFCTag)
admin.site.register(Branch)