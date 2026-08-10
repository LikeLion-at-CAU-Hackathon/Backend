from django.shortcuts import render
import uuid

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import VisitSession, VisitHistory
from products.models import Product
from .serializers import VisitHistorySerializer, VisitSessionSerializer


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