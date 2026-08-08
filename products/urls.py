from django.urls import path
from .views import *

urlpatterns = [
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("<int:product_id>/stock/", ProductStockAPIView.as_view(), name="product-stock"),
]