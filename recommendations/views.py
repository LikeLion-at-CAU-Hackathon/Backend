from django.shortcuts import render
import uuid

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


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


class StyleProfileRetrieveAPIView(APIView):

    def get(self, request, session_id):
        visit_session = get_object_or_404(
            VisitSession,
            id=session_id
        )

        profile = get_object_or_404(
            StyleProfile,
            visit_session=visit_session
        )

        serializer = StyleProfileSerializer(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

# mock Look 생성 API
class MockStylingResultCreateAPIView(APIView):

    def post(self, request, profile_id):
        profile = get_object_or_404(
            StyleProfile,
            id=profile_id
        )

        product1 = get_object_or_404(Product, id=1)
        product2 = get_object_or_404(Product, id=2)
        product3 = get_object_or_404(Product, id=3)
        product4 = get_object_or_404(Product, id=4)

        # 재시도했을 때 Look이 계속 중복 생성되는 걸 방지
        StylingResult.objects.filter(
            style_profile=profile
        ).delete()

        look1 = StylingResult.objects.create(
            style_profile=profile,
            look_order=1,
            title="Business Casual Look",
            subtitle="Classic Monogram Balance",
            description="A refined business casual styling with a classic MCM accent.",
            reason="Recommended based on your current interest in classic and compact pieces."
        )

        StylingItem.objects.create(
            styling_result=look1,
            product=product1,
            order=1,
            type="MAIN"
        )

        StylingItem.objects.create(
            styling_result=look1,
            product=product3,
            order=2,
            type="MATCH"
        )

        look2 = StylingResult.objects.create(
            style_profile=profile,
            look_order=2,
            title="Weekend Casual Look",
            subtitle="Relaxed Signature Style",
            description="A relaxed weekend combination with a signature MCM accent.",
            reason="Recommended to match your interest in versatile everyday styling."
        )

        StylingItem.objects.create(
            styling_result=look2,
            product=product2,
            order=1,
            type="MAIN"
        )

        StylingItem.objects.create(
            styling_result=look2,
            product=product4,
            order=2,
            type="ACCENT"
        )

        look3 = StylingResult.objects.create(
            style_profile=profile,
            look_order=3,
            title="Travel Look",
            subtitle="Compact Travel Styling",
            description="A practical travel look centered around compact accessories.",
            reason="Recommended based on your current interest in compact and functional pieces."
        )

        StylingItem.objects.create(
            styling_result=look3,
            product=product1,
            order=1,
            type="MAIN"
        )

        StylingItem.objects.create(
            styling_result=look3,
            product=product2,
            order=2,
            type="ACCENT"
        )

        looks = StylingResult.objects.filter(
            style_profile=profile
        ).order_by("look_order")

        serializer = StylingResultSerializer(
            looks,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )