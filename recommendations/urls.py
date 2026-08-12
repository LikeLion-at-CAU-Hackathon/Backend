from django.urls import path

from .views import *


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

    # path(
    #     "sessions/<int:session_id>/analyze/",
    #     MockStyleAnalyzeAPIView.as_view(),
    #     name="style-analyze",
    # ),
    
    path(
        "sessions/<int:session_id>/profile/",
        StyleProfileRetrieveAPIView.as_view(),
        name="style-profile-detail",
    ),
    path(
        "profiles/<int:profile_id>/looks/",
        MockStylingResultCreateAPIView.as_view(),
        name="mock-styling-result-create",
    ),

    path(
        "profiles/<int:profile_id>/recommendations/",
        MockRecommendationCreateAPIView.as_view(),
        name="mock-recommendation-create",
    ),

    path(
    "sessions/<int:session_id>/analyze/",
    StyleAnalysisAPIView.as_view(),
    name="style-analysis",
    ),

    path(
    "sessions/<int:session_id>/saved-products/",
    SavedProductCreateAPIView.as_view(),
    name="saved-product-create",
    ),
    
]