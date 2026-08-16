from django.db.models import Prefetch
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import *
from .models import *
from .services import *

class ProductAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    queryset = Product.objects.prefetch_related(
        "details__images",
        "details__stocks__branch",
    )

class ProductStockAPIView(ListAPIView):
    serializer_class = StockSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        return Stock.objects.filter(
            detail__product_id=product_id
        ).select_related("branch")
        
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



class ProductBackgroundAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductBackgroundSerializer
    lookup_url_kwarg = "product_id"

class ProductMaterialAPIView(ListAPIView):
    serializer_class = MaterialSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        return Material.objects.filter(
            products__product_id=product_id
        ).order_by("order")
        
class ProductCareGuideAPIView(ListAPIView):
    serializer_class = CareGuideSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        return Material.objects.filter(
            products__product_id=product_id
        ).order_by("order")

class AIAssistantAPIView(APIView):

    def post(self, request, product_id):

        serializer = AIAssistantRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(
            Product,
            id=product_id
        )

        product_context = build_ai_assistant_context(
            product
        )

        answer = ask_ai_assistant(
            question=serializer.validated_data["question"],
            product_context=product_context,
        )
        
        response_serializer = AIAssistantResponseSerializer(
            data={
                "answer": answer
            }
        )
        response_serializer.is_valid(raise_exception=True)

        return Response(
            response_serializer.validated_data
        )