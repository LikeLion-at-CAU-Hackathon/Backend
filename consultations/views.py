from rest_framework.generics import CreateAPIView

from .models import ConsultationRequest
from .serializers import ConsultationRequestSerializer


class ConsultationRequestCreateAPIView(CreateAPIView):
    queryset = ConsultationRequest.objects.all()
    serializer_class = ConsultationRequestSerializer
    
    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        session_key = self.request.session.session_key

        if not session_key:
            self.request.session.create()
            session_key = self.request.session.session_key

        serializer.save(
            user=user,
            session_key=session_key,
        )
