from django.urls import path

from .views import *


urlpatterns = [

    # 현재 방문 세션 확인/생성
    # 테스트용으로 남겨둬도 됨
    path(
        "sessions/",
        VisitSessionCreateAPIView.as_view(),
        name="visit-session",
    ),

    # 방문 기록 조회 / 추가
    path(
        "sessions/history/",
        VisitHistoryAPIView.as_view(),
        name="visit-history",
    ),

    # 스타일 분석 실행
    path(
        "sessions/analyze/",
        StyleAnalysisAPIView.as_view(),
        name="style-analysis",
    ),

    # 스타일 분석 결과 조회
    path(
        "sessions/result/",
        StyleResultAPIView.as_view(),
        name="style-result",
    ),

    # Look 상세 조회
    path(
        "looks/<int:look_id>/",
        LookDetailAPIView.as_view(),
        name="look-detail",
    ),

    # 저장 제품 추가 / 삭제
    path(
        "sessions/saved-products/<int:product_id>/",
        SavedProductAPIView.as_view(),
        name="saved-product",
    ),

    # 저장 제품 전체 조회
    path(
        "sessions/saved-products/",
        SavedProductListAPIView.as_view(),
        name="saved-product-list",
    ),

    # 특정 저장 제품 분석 결과 조회
    path(
        "sessions/saved-products/<int:product_id>/analysis/",
        SavedProductAnalysisAPIView.as_view(),
        name="saved-product-analysis",
    ),
]