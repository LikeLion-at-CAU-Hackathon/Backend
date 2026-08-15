from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from products.models import Product
from recommendations.models import VisitSession

from .models import ConsultationRequest
from .serializers import ConsultationRequestSerializer


class ConsultationRequestCreateAPIView(CreateAPIView):
    queryset = ConsultationRequest.objects.all()
    serializer_class = ConsultationRequestSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        product = get_object_or_404(
            Product,
            id=self.kwargs["product_id"],
        )

        session_key = self.request.headers.get("X-Session-Key")

        session = get_object_or_404(
            VisitSession,
            session_key=session_key,
        )

        serializer.save(
            product=product,
            session=session,
        )