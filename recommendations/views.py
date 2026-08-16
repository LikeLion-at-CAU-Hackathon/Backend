import uuid

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from .models import StyleProfile, VisitSession, Look,  VisitHistory
from .services import analyze_visit_session
from .serializers import (
    StyleProfileSerializer,
    LookSerializer,
    LookDetailSerializer,
    VisitSessionSerializer,
    VisitHistorySerializer,
)

# 분석, 저장 APIView
class StyleAnalysisAPIView(APIView):

    def post(self, request, session_id):
        visit_session = get_object_or_404(
            VisitSession,
            id=session_id
        )

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


# 스타일 분석 결과 조회 APIView
class StyleResultAPIView(APIView):

    def get(self, request, session_id):
        visit_session = get_object_or_404(
            VisitSession,
            id=session_id
        )

        style_profile = get_object_or_404(
            StyleProfile,
            visit_session=visit_session
        )

        serializer = StyleProfileSerializer(
            style_profile
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )

# 개별 Look 상세 조회 APIView
class LookDetailAPIView(APIView):

    def get(self, request, look_id):
        look = get_object_or_404(
            Look,
            id=look_id
        )

        serializer = LookDetailSerializer(
            look,
            context={"request": request}
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )


class VisitSessionCreateAPIView(APIView):

    def post(self, request):
        visit_session = VisitSession.objects.create(
            session_key=str(uuid.uuid4())
        )

        serializer = VisitSessionSerializer(
            visit_session
        )

        return Response(
            {
                "success": True,
                "session": serializer.data,
            },
            status=status.HTTP_201_CREATED
        )

class VisitHistoryAPIView(APIView):

    def get(self, request, session_id):
        visit_session = get_object_or_404(
            VisitSession,
            id=session_id
        )

        histories = (
            VisitHistory.objects
            .filter(visit_session=visit_session)
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

    def post(self, request, session_id):
        visit_session = get_object_or_404(
            VisitSession,
            id=session_id
        )

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
            .filter(visit_session=visit_session)
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