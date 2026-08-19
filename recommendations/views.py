from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Product

from .models import (
    SavedProduct,
    StyleProfile,
    VisitSession,
    Look,
    VisitHistory,
)

from .services import analyze_visit_session

from .serializers import (
    StyleProfileSerializer,
    LookSerializer,
    LookDetailSerializer,
    SavedProductSerializer,
    VisitSessionSerializer,
    VisitHistorySerializer,
)

from .utils import get_or_create_visit_session


# ==========================================
# 스타일 분석 실행
# ==========================================

class StyleAnalysisAPIView(APIView):

    def post(self, request):

        visit_session = get_or_create_visit_session(request)

        try:
            result = analyze_visit_session(
                visit_session
            )

        except ValueError as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "profile": StyleProfileSerializer(
                    result["profile"]
                ).data,
                "looks": LookSerializer(
                    result["looks"],
                    many=True
                ).data,
            },
            status=status.HTTP_200_OK
        )


# ==========================================
# 스타일 분석 결과 조회
# ==========================================

class StyleResultAPIView(APIView):

    def get(self, request):

        visit_session = get_or_create_visit_session(request)

        style_profile = (
            StyleProfile.objects
            .filter(
                visit_session=visit_session
            )
            .order_by("-created_at")
            .first()
        )

        if style_profile is None:
            return Response(
                {
                    "success": False,
                    "message": "스타일 분석 결과가 없습니다.",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StyleProfileSerializer(
            style_profile,
            context={
                "request": request
            }
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# ==========================================
# 개별 Look 상세 조회
# ==========================================

class LookDetailAPIView(APIView):

    def get(self, request, look_id):

        look = get_object_or_404(
            Look,
            id=look_id
        )

        serializer = LookDetailSerializer(
            look,
            context={
                "request": request
            }
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# ==========================================
# 현재 방문 세션 확인/생성
#
# 필수 API는 아님.
# VisitHistoryAPIView 등이 알아서 세션을 생성하므로
# 테스트용 또는 세션 확인용으로 남겨둘 수 있음.
# ==========================================

class VisitSessionCreateAPIView(APIView):

    def post(self, request):

        visit_session = get_or_create_visit_session(request)

        serializer = VisitSessionSerializer(
            visit_session
        )

        return Response(
            {
                "success": True,
                "session": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# ==========================================
# 방문 기록 조회 / 추가
# ==========================================

class VisitHistoryAPIView(APIView):

    def get(self, request):

        visit_session = get_or_create_visit_session(request)

        histories = (
            VisitHistory.objects
            .filter(
                visit_session=visit_session
            )
            .select_related("product")
            .order_by("sequence")
        )

        serializer = VisitHistorySerializer(
            histories,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": histories.count(),
                "histories": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):

        visit_session = get_or_create_visit_session(request)

        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {
                    "success": False,
                    "message": "product_id가 필요합니다.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(
            Product,
            id=product_id
        )

        last_history = (
            VisitHistory.objects
            .filter(
                visit_session=visit_session
            )
            .order_by("-sequence")
            .first()
        )

        next_sequence = (
            last_history.sequence + 1
            if last_history
            else 1
        )

        visit_history = VisitHistory.objects.create(
            visit_session=visit_session,
            product=product,
            sequence=next_sequence,
        )

        serializer = VisitHistorySerializer(
            visit_history
        )

        return Response(
            {
                "success": True,
                "history": serializer.data,
            },
            status=status.HTTP_201_CREATED
        )


# ==========================================
# 저장 제품 추가 / 삭제
# ==========================================

class SavedProductAPIView(APIView):

    def post(
        self,
        request,
        product_id
    ):

        visit_session = get_or_create_visit_session(request)

        product = get_object_or_404(
            Product,
            id=product_id
        )

        saved_product, created = (
            SavedProduct.objects.get_or_create(
                visit_session=visit_session,
                product=product
            )
        )

        return Response(
            {
                "success": True,
                "saved": True,
                "created": created,
            },
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )

    def delete(
        self,
        request,
        product_id
    ):

        visit_session = get_or_create_visit_session(request)

        saved_product = get_object_or_404(
            SavedProduct,
            visit_session=visit_session,
            product_id=product_id
        )

        saved_product.delete()

        return Response(
            {
                "success": True,
                "saved": False,
            },
            status=status.HTTP_200_OK
        )


# ==========================================
# 저장 제품 전체 조회
# ==========================================

class SavedProductListAPIView(APIView):

    def get(self, request):

        visit_session = get_or_create_visit_session(request)

        saved_products = (
            SavedProduct.objects
            .filter(
                visit_session=visit_session
            )
            .select_related("product")
            .order_by("-saved_at")
        )

        serializer = SavedProductSerializer(
            saved_products,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": saved_products.count(),
                "saved_products": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# ==========================================
# 저장 제품의 분석 결과 조회
# ==========================================

class SavedProductAnalysisAPIView(APIView):

    def get(
        self,
        request,
        product_id
    ):

        visit_session = get_or_create_visit_session(request)

        product = get_object_or_404(
            Product,
            id=product_id
        )

        get_object_or_404(
            SavedProduct,
            visit_session=visit_session,
            product=product
        )

        profile = (
            StyleProfile.objects
            .filter(
                visit_session=visit_session,
                main_product=product
            )
            .order_by("-created_at")
            .first()
        )

        if profile is None:
            return Response(
                {
                    "success": False,
                    "message": (
                        "아직 저장된 분석 결과가 없습니다."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StyleProfileSerializer(
            profile,
            context={
                "request": request
            }
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )