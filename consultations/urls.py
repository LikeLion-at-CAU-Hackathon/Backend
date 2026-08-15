from django.urls import path

from .views import ConsultationRequestCreateAPIView


urlpatterns = [
    path(
        "products/<int:product_id>/",
        ConsultationRequestCreateAPIView.as_view(),
        name="consultation-request-create",
    ),
]