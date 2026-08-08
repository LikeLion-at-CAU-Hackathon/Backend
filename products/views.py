from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .serializers import *
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

class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductStockAPIView(ListAPIView):
    serializer_class = StockSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        return Stock.objects.filter(
            product_id=product_id
        ).select_related("branch")