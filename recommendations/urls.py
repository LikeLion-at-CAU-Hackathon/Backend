from django.urls import path

from .views import VisitHistoryCreateAPIView, VisitSessionCreateAPIView


urlpatterns = [
    path(
        "sessions/",
        VisitSessionCreateAPIView.as_view(),
        name="visit-session-create",
    ),

    path(
    "sessions/<int:session_id>/history/",
    VisitHistoryCreateAPIView.as_view(),
    name="visit-history-create",
),
]