from django.urls import path
from .views import *

urlpatterns = [
    path(
        "compare/",
        ProductCompareAPIView.as_view(),
        name="product-compare",
    ),
    
    path(
        "<int:pk>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),

    path(
        "<int:product_id>/stock/",
        ProductStockAPIView.as_view(),
        name="product-stock",
    ),

    path(
        "<int:product_id>/sizes/",
        ProductSizeAPIView.as_view(),
        name="product-sizes",
    ),
]