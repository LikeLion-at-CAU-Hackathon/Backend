from django.shortcuts import render
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import VisitSession
from .serializers import VisitSessionSerializer


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