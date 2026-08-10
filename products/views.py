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
        
class AIDocentAPIView(APIView):
    def post(self, request, product_id):
        question = request.data.get("question")

        if not question:
            return Response(
                {"detail": "질문을 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(
            Product,
            id=product_id
        )

        # 제품 Story
        story = getattr(product, "story", None)

        # 제품 Material
        materials = product.materials.all()

        # 제품 Care Guide
        care_guide = getattr(product, "care_guide", None)

        # AI에게 전달할 제품 정보
        product_context = {
            "name": product.name,
            "color": product.color,
            "size": product.size,
            "specs": product.specs,
            "story": story.sections if story else [],
            "materials": [
                {
                    "name": material.name,
                    "location": material.location,
                    "description": material.description,
                }
                for material in materials
            ],
            "care_guide": care_guide.contents if care_guide else [],
        }

        print(product_context)

        # 일단 테스트
        answer = "제품 정보를 확인했습니다."

        conversation = AIConversation.objects.create(
            product=product,
            question=question,
            answer=answer
        )

        return Response(
            AIConversationSerializer(conversation).data,
            status=status.HTTP_200_OK
        )