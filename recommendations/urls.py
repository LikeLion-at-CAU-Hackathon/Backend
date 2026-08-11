from django.urls import path

from .views import StyleAnalyzeAPIView, VisitHistoryCreateAPIView, VisitSessionCreateAPIView


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

    path(
        "sessions/<int:session_id>/analyze/",
        StyleAnalyzeAPIView.as_view(),
        name="style-analyze",
    ),
]