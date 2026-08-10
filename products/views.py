from django.db.models import Prefetch
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .serializers import *
from .models import *

class ProductAPIView(RetrieveAPIView):
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
        ).order_by("size")
        
class ProductCompareAPIView(ListAPIView):
    serializer_class = ProductCompareSerializer

    def get_queryset(self):
        ids = self.request.query_params.get("ids")
        branch_id = self.request.query_params.get("branch_id")

        if not ids:
            return Product.objects.none()

        product_ids = ids.split(",")

        queryset = Product.objects.filter(
            id__in=product_ids
        )

        if branch_id:
            queryset = queryset.prefetch_related(
                Prefetch(
                    "stocks",
                    queryset=Stock.objects.filter(
                        branch_id=branch_id
                    ).select_related("branch")
                )
            )

        return queryset



class ProductStoryAPIView(RetrieveAPIView):
    serializer_class = StorySerializer

    def get_object(self):
        product_id = self.kwargs["product_id"]

        return get_object_or_404(
            Story,
            product_id=product_id
        )

class ProductMaterialAPIView(ListAPIView):
    serializer_class = MaterialSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        return Material.objects.filter(
            product_id=product_id
        )

class ProductCareGuideAPIView(RetrieveAPIView):
    serializer_class = CareGuideSerializer

    def get_object(self):
        product_id = self.kwargs["product_id"]

        return get_object_or_404(
            CareGuide,
            product_id=product_id
        )