from django.shortcuts import render
import uuid

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import StyleProfile, VisitSession, VisitHistory
from products.models import Product
from .serializers import StyleProfileSerializer, VisitHistorySerializer, VisitSessionSerializer


class VisitSessionCreateAPIView(APIView):

    def post(self, request):
        visit_session = VisitSession.objects.create(
            session_key=str(uuid.uuid4())
        )

        serializer = VisitSessionSerializer(visit_session)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class VisitHistoryCreateAPIView(APIView):

    def post(self, request, session_id):
        visit_session = get_object_or_404(
            VisitSession,
            id=session_id
        )

        product = get_object_or_404(
            Product,
            id=request.data.get("product_id")
        )

        sequence = (
            VisitHistory.objects
            .filter(visit_session=visit_session)
            .count()
            + 1
        )

        visit_history = VisitHistory.objects.create(
            visit_session=visit_session,
            product=product,
            sequence=sequence
        )

        serializer = VisitHistorySerializer(visit_history)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class StyleAnalyzeAPIView(APIView):

    def post(self, request, session_id):
        visit_session = get_object_or_404(
            VisitSession,
            id=session_id
        )

        histories = VisitHistory.objects.filter(
            visit_session=visit_session
        )

        if not histories.exists():
            return Response(
                {
                    "success": False,
                    "message": "분석할 제품이 없습니다."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if histories.count() == 1:
            mode = StyleProfile.AnalysisMode.SINGLE_PRODUCT
        else:
            mode = StyleProfile.AnalysisMode.BEHAVIOR

        profile, created = StyleProfile.objects.update_or_create(
            visit_session=visit_session,
            defaults={
                "summary": "Current browsing activity shows an interest in refined and versatile styling.",
                "tags": [
                    "Warm Tone Interest",
                    "Compact",
                    "Classic"
                ],
                "analysis_mode": mode
            }
        )

        serializer = StyleProfileSerializer(profile)

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )