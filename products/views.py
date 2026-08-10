from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .serializers import *
from .models import *

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
        
class ProductSizeAPIView(ListAPIView):
    serializer_class = ProductSizeSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        product = get_object_or_404(
            Product,
            id=product_id
        )

        return Product.objects.filter(
            group_id=product.group_id
        )
        
class ProductCompareAPIView(ListAPIView):
    serializer_class = ProductCompareSerializer

    def get_queryset(self):
        ids = self.request.query_params.get("ids")

        if not ids:
            return Product.objects.none()

        product_ids = ids.split(",")

        return Product.objects.filter(
            id__in=product_ids
        ).select_related("product_detail")