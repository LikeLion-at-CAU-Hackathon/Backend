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
        VisitHistoryAPIView.as_view(),
        name="visit-history",
    ),
    

    path(
        "sessions/<int:session_id>/analyze/",
        StyleAnalysisAPIView.as_view(),
        name="style-analysis"
    ),

    path(
        "sessions/<int:session_id>/result/",
        StyleResultAPIView.as_view(),
        name="style-result"
    ),

    path(
        "looks/<int:look_id>/",
        LookDetailAPIView.as_view(),
        name="look-detail"
    ),

    path(
        "sessions/<int:session_id>/saved-products/<int:product_id>/",
        SavedProductAPIView.as_view(),
        name="saved-product"
    ),

    path(
        "sessions/<int:session_id>/saved-products/",
        SavedProductListAPIView.as_view(),
        name="saved-product-list"
    ),

    path(
        "sessions/<int:session_id>/saved-products/<int:product_id>/analysis/",
        SavedProductAnalysisAPIView.as_view(),
        name="saved-product-analysis"
    ),
]