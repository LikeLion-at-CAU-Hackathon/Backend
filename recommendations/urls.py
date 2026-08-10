from django.urls import path

from .views import VisitSessionCreateAPIView


urlpatterns = [
    path(
        "sessions/",
        VisitSessionCreateAPIView.as_view(),
        name="visit-session-create",
    ),
]