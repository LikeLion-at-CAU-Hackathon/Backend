from django.db.models import Prefetch
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *

class ProductAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductSizeAPIView(ListAPIView):
    serializer_class = ProductSizeSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        return ProductDetail.objects.filter(
            product_id=product_id
        ).order_by("size")
        
class ProductSizeAPIView(ListAPIView):
    serializer_class = ProductSizeSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        return ProductDetail.objects.filter(
            product_id=product_id
        ).order_by("size")
        
class ProductCompareAPIView(ListAPIView):
    serializer_class = ProductCompareSerializer

    def get_queryset(self):
        ids = self.request.query_params.get("ids")
        branch_id = self.request.query_params.get("branch_id")

        if not ids:
            return ProductDetail.objects.none()

        detail_ids = ids.split(",")

        queryset = ProductDetail.objects.filter(
            id__in=detail_ids
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
        else:
            queryset = queryset.prefetch_related(
                "stocks__branch"
            )

        return queryset


