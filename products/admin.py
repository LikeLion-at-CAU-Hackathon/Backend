from django.contrib import admin
from .models import *

admin.site.register(ProductGroup)
admin.site.register(Collection)
admin.site.register(Product)
admin.site.register(Branch)
admin.site.register(Stock)
admin.site.register(ProductImage)
admin.site.register(NFCTag)

admin.site.register(Story)
admin.site.register(Material)
admin.site.register(CareGuide)