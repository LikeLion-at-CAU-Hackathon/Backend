from django.urls import path

from .views import ConsultationRequestCreateAPIView


urlpatterns = [
    path(
        "",
        ConsultationRequestCreateAPIView.as_view(),
        name="consultation-request-create",
    ),
]