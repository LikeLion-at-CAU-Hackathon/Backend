from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import StyleProfile, VisitSession, Look
from .services import analyze_visit_session
from .serializers import (
    StyleProfileSerializer,
    LookSerializer,
    LookDetailSerializer,
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

        try:
            profile = visit_session.style_profile
        except StyleProfile.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "아직 스타일 분석 결과가 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        looks = (
            profile.looks
            .prefetch_related(
                "style_chips",
                "look_products__product"
            )
            .all()
        )

        return Response(
            {
                "success": True,
                "profile": StyleProfileSerializer(profile).data,
                "looks": LookSerializer(
                    looks,
                    many=True
                ).data,
            },
            status=status.HTTP_200_OK
        )

# 개별 Look 상세 조회 APIView
class LookDetailAPIView(APIView):

    def get(self, request, look_id):
        look = get_object_or_404(
            Look.objects
            .prefetch_related(
                "style_chips",
                "look_products__product",
            ),
            id=look_id
        )

        serializer = LookDetailSerializer(look)

        return Response(
            {
                "success": True,
                "look": serializer.data,
            },
            status=status.HTTP_200_OK
        )