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
        ProductAPIView.as_view(),
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
    
    path(
    "<int:product_id>/story/",
    ProductStoryAPIView.as_view(),
    name="product-story",
    ),

    path(
        "<int:product_id>/materials/",
        ProductMaterialAPIView.as_view(),
        name="product-materials",
    ),

    path(
        "<int:product_id>/care-guide/",
        ProductCareGuideAPIView.as_view(),
        name="product-care-guide",
    ),
    
    path(
        "<int:product_id>/ai-docent/",
        AIDocentAPIView.as_view(),
        name="ai-docent",
    ),
]