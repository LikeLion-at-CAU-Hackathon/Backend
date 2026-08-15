# from django.shortcuts import render
# import uuid

# from django.shortcuts import get_object_or_404
# from django.db import transaction
# from recommendations.services import *
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from .models import *
# from .serializers import *


# class VisitSessionCreateAPIView(APIView):

#     def post(self, request):
#         visit_session = VisitSession.objects.create(
#             session_key=str(uuid.uuid4())
#         )

#         serializer = VisitSessionSerializer(visit_session)

#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED
#         )

# class VisitHistoryCreateAPIView(APIView):

#     def post(self, request, session_id):
#         visit_session = get_object_or_404(
#             VisitSession,
#             id=session_id
#         )

#         product = get_object_or_404(
#             Product,
#             id=request.data.get("product_id")
#         )

#         sequence = (
#             VisitHistory.objects
#             .filter(visit_session=visit_session)
#             .count()
#             + 1
#         )

#         visit_history = VisitHistory.objects.create(
#             visit_session=visit_session,
#             product=product,
#             sequence=sequence
#         )

#         serializer = VisitHistorySerializer(visit_history)

#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED
#         )


# class StyleProfileRetrieveAPIView(APIView):

#     def get(self, request, session_id):
#         visit_session = get_object_or_404(
#             VisitSession,
#             id=session_id
#         )

#         profile = get_object_or_404(
#             StyleProfile,
#             visit_session=visit_session
#         )

#         serializer = StyleProfileSerializer(profile)

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

# # mock Look 생성 API
# class MockLookCreateAPIView(APIView):

#     def post(self, request, profile_id):
#         profile = get_object_or_404(
#             StyleProfile,
#             id=profile_id
#         )

#         product1 = get_object_or_404(Product, id=1)
#         product2 = get_object_or_404(Product, id=2)
#         product3 = get_object_or_404(Product, id=3)
#         product4 = get_object_or_404(Product, id=4)

#         # 재시도했을 때 Look이 계속 중복 생성되는 걸 방지
#         Look.objects.filter(
#             style_profile=profile
#         ).delete()

#         look1 = Look.objects.create(
#             style_profile=profile,
#             look_order=1,
#             title="Business Casual Look",
#             subtitle="Classic Monogram Balance",
#             description="A refined business casual styling with a classic MCM accent.",
#             reason="Recommended based on your current interest in classic and compact pieces."
#         )

#         # LookItem.objects.create(
#         #     styling_result=look1,
#         #     product=product1,
#         #     order=1,
#         #     type="MAIN"
#         # )

#         # LookItem.objects.create(
#         #     styling_result=look1,
#         #     product=product3,
#         #     order=2,
#         #     type="MATCH"
#         # )

#         look2 = Look.objects.create(
#             style_profile=profile,
#             look_order=2,
#             title="Weekend Casual Look",
#             subtitle="Relaxed Signature Style",
#             description="A relaxed weekend combination with a signature MCM accent.",
#             reason="Recommended to match your interest in versatile everyday styling."
#         )

#         LookItem.objects.create(
#             styling_result=look2,
#             product=product2,
#             order=1,
#             type="MAIN"
#         )

#         LookItem.objects.create(
#             styling_result=look2,
#             product=product4,
#             order=2,
#             type="ACCENT"
#         )

#         look3 = Look.objects.create(
#             style_profile=profile,
#             look_order=3,
#             title="Travel Look",
#             subtitle="Compact Travel Styling",
#             description="A practical travel look centered around compact accessories.",
#             reason="Recommended based on your current interest in compact and functional pieces."
#         )

#         LookItem.objects.create(
#             styling_result=look3,
#             product=product1,
#             order=1,
#             type="MAIN"
#         )

#         LookItem.objects.create(
#             styling_result=look3,
#             product=product2,
#             order=2,
#             type="ACCENT"
#         )

#         looks = Look.objects.filter(
#             style_profile=profile
#         ).order_by("look_order")

#         serializer = LookSerializer(
#             looks,
#             many=True
#         )

#         return Response(
#             {
#                 "success": True,
#                 "data": serializer.data
#             },
#             status=status.HTTP_201_CREATED
#         )

# class MockRecommendationCreateAPIView(APIView):

#     def post(self, request, profile_id):
#         profile = get_object_or_404(
#             StyleProfile,
#             id=profile_id
#         )

#         product1 = get_object_or_404(Product, id=1)
#         product2 = get_object_or_404(Product, id=2)
#         product3 = get_object_or_404(Product, id=3)
#         product4 = get_object_or_404(Product, id=4)

#         # 재호출 시 추천이 계속 쌓이지 않도록 기존 결과 삭제
#         RecommendationResult.objects.filter(
#             style_profile=profile
#         ).delete()

#         RecommendationResult.objects.create(
#             style_profile=profile,
#             product=product1,
#             type=RecommendationResult.RecommendationType.SIMILAR,
#             reason="Recommended for its classic and compact styling.",
#             score=100
#         )

#         RecommendationResult.objects.create(
#             style_profile=profile,
#             product=product2,
#             type=RecommendationResult.RecommendationType.SIMILAR,
#             reason="Recommended for its warm tone and signature monogram details.",
#             score=80
#         )

#         RecommendationResult.objects.create(
#             style_profile=profile,
#             product=product4,
#             type=RecommendationResult.RecommendationType.NEW,
#             reason="Recommended as a fresh accent piece that complements your current interests.",
#             score=60
#         )

#         recommendations = RecommendationResult.objects.filter(
#             style_profile=profile
#         ).order_by("-score")

#         serializer = RecommendationResultSerializer(
#             recommendations,
#             many=True
#         )

#         return Response(
#             {
#                 "success": True,
#                 "data": serializer.data
#             },
#             status=status.HTTP_201_CREATED
#         )


# # Style Analysis APIView
# class StyleAnalysisAPIView(APIView):

#     @transaction.atomic
#     def post(self, request, session_id):

#         # 1. 방문 세션 확인
#         visit_session = get_object_or_404(
#             VisitSession,
#             id=session_id
#         )

#         # 2. 이번 방문의 NFC 탐색 기록 조회
#         histories = VisitHistory.objects.filter(
#             visit_session=visit_session
#         ).select_related("product")

#         # 이번 방문에서 저장한 제품 조회
#         saved_products = SavedProduct.objects.filter(
#             visit_session=visit_session
#         ).select_related("product")


#         # 3. NFC 태그와 저장 제품이 모두 없으면 분석 불가
#         if not histories.exists() and not saved_products.exists():
#             return Response(
#                 {
#                     "success": False,
#                     "message": "스타일 분석을 진행할 수 없습니다."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )


#         # 4. NFC 태그 개수 기준으로 분석 방식 결정
#         history_count = histories.count()

#         if history_count <= 1:
#             analysis_mode = StyleProfile.AnalysisMode.SINGLE_PRODUCT
#         else:
#             analysis_mode = StyleProfile.AnalysisMode.BEHAVIOR

#         # 5. AI 분석에 사용할 제품 목록 구성
#         history_products = [
#             history.product
#             for history in histories
#         ]

#         saved_products_list = [
#             saved.product
#             for saved in saved_products
#         ]

#         analysis_products = history_products + saved_products_list

#         # NFC로 본 제품과 저장한 제품이 겹칠 수 있으므로 중복 제거
#         product_map = {
#             product.id: product
#             for product in analysis_products
#         }

#         analysis_products = list(product_map.values())

#         # AI에게 넘길 수 있는 dict 형태로 변환
#         product_context = build_product_context(
#             analysis_products
#         )

#         # AI를 통해 StyleProfile 생성
#         ai_profile = generate_style_profile(
#             product_context,
#             analysis_mode
#         )

#         # # test용 Mock StyleProfile 생성
#         # ai_profile = {
#         #     "summary": "Current browsing activity shows an interest in refined and versatile styling.",
#         #     "tags": [
#         #         "Classic",
#         #         "Compact",
#         #         "Warm Tone Interest"
#         #     ]
#         # }

#         profile, created = StyleProfile.objects.update_or_create(
#             visit_session=visit_session,
#             defaults={
#                 "summary": ai_profile["summary"],
#                 "tags": ai_profile["tags"],
#                 "analysis_mode": analysis_mode
#             }
#         )

#         # 재시도 시 기존 추천 결과 삭제
#         Look.objects.filter(
#             style_profile=profile
#         ).delete()

#         RecommendationResult.objects.filter(
#             style_profile=profile
#         ).delete()

#         # 테스트용 상품
#         product1 = get_object_or_404(Product, id=1)
#         product2 = get_object_or_404(Product, id=2)
#         product3 = get_object_or_404(Product, id=3)
#         product4 = get_object_or_404(Product, id=4)

#         # 6. Look 1
#         look1 = Look.objects.create(
#             style_profile=profile,
#             look_order=1,
#             title="Business Casual Look",
#             subtitle="Classic Monogram Balance",
#             description=(
#                 "A refined business casual styling "
#                 "with a classic MCM accent."
#             ),
#             reason=(
#                 "Recommended based on your current interest "
#                 "in classic and compact pieces."
#             )
#         )

#         LookItem.objects.create(
#             styling_result=look1,
#             product=product1,
#             order=1,
#             type="MAIN"
#         )

#         LookItem.objects.create(
#             styling_result=look1,
#             product=product3,
#             order=2,
#             type="MATCH"
#         )

#         # 7. Look 2
#         look2 = Look.objects.create(
#             style_profile=profile,
#             look_order=2,
#             title="Weekend Casual Look",
#             subtitle="Relaxed Signature Style",
#             description=(
#                 "A relaxed weekend combination "
#                 "with a signature MCM accent."
#             ),
#             reason=(
#                 "Recommended to match your interest "
#                 "in versatile everyday styling."
#             )
#         )

#         LookItem.objects.create(
#             styling_result=look2,
#             product=product2,
#             order=1,
#             type="MAIN"
#         )

#         LookItem.objects.create(
#             styling_result=look2,
#             product=product4,
#             order=2,
#             type="ACCENT"
#         )

#         # 8. Look 3
#         look3 = Look.objects.create(
#             style_profile=profile,
#             look_order=3,
#             title="Travel Look",
#             subtitle="Compact Travel Styling",
#             description=(
#                 "A practical travel look centered "
#                 "around compact accessories."
#             ),
#             reason=(
#                 "Recommended based on your current interest "
#                 "in compact and functional pieces."
#             )
#         )

#         LookItem.objects.create(
#             styling_result=look3,
#             product=product1,
#             order=1,
#             type="MAIN"
#         )

#         LookItem.objects.create(
#             styling_result=look3,
#             product=product2,
#             order=2,
#             type="ACCENT"
#         )

#         # 9. FOR YOU
#         RecommendationResult.objects.create(
#             style_profile=profile,
#             product=product1,
#             type=RecommendationResult.RecommendationType.SIMILAR,
#             reason="Recommended for its classic and compact styling.",
#             score=100
#         )

#         RecommendationResult.objects.create(
#             style_profile=profile,
#             product=product2,
#             type=RecommendationResult.RecommendationType.SIMILAR,
#             reason=(
#                 "Recommended for its warm tone "
#                 "and signature monogram details."
#             ),
#             score=80
#         )

#         RecommendationResult.objects.create(
#             style_profile=profile,
#             product=product4,
#             type=RecommendationResult.RecommendationType.NEW,
#             reason=(
#                 "Recommended as a fresh accent piece "
#                 "that complements your current interests."
#             ),
#             score=60
#         )

#         # 10. 결과가 정말 만들어졌는지 검사
#         look_count = Look.objects.filter(
#             style_profile=profile
#         ).count()

#         recommendation_count = RecommendationResult.objects.filter(
#             style_profile=profile
#         ).count()

#         if look_count != 3 or recommendation_count == 0:
#             return Response(
#                 {
#                     "success": False,
#                     "message": "스타일 분석을 불러오지 못했어요. 다시 시도해주세요."
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         return Response(
#             {
#                 "success": True,
#                 "profile_id": profile.id,
#                 "analysis_mode": profile.analysis_mode,
#                 "message": "Style analysis completed."
#             },
#             status=status.HTTP_200_OK
#         )


# class SavedProductCreateAPIView(APIView):

#     def post(self, request, session_id):
#         visit_session = get_object_or_404(
#             VisitSession,
#             id=session_id
#         )

#         product = get_object_or_404(
#             Product,
#             id=request.data.get("product_id")
#         )

#         saved_product, created = SavedProduct.objects.get_or_create(
#             visit_session=visit_session,
#             product=product
#         )

#         serializer = SavedProductSerializer(saved_product)

#         return Response(
#             {
#                 "success": True,
#                 "created": created,
#                 "data": serializer.data
#             },
#             status=(
#                 status.HTTP_201_CREATED
#                 if created
#                 else status.HTTP_200_OK
#             )
#         )


# # 통합 조회 APIView
# class StyleResultRetrieveAPIView(APIView):

#     def get(self, request, session_id):
#         visit_session = get_object_or_404(
#             VisitSession,
#             id=session_id
#         )

#         profile = get_object_or_404(
#             StyleProfile,
#             visit_session=visit_session
#         )

#         looks = Look.objects.filter(
#             style_profile=profile
#         ).prefetch_related("items").order_by("look_order")

#         recommendations = RecommendationResult.objects.filter(
#             style_profile=profile
#         ).order_by("-score")

#         # 3.2 화면에 필요한 결과가 모두 있는지 확인
#         if looks.count() != 3 or not recommendations.exists():
#             return Response(
#                 {
#                     "success": False,
#                     "message": "스타일 분석 결과가 완성되지 않았습니다."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         return Response(
#             {
#                 "success": True,
#                 "profile": StyleProfileSerializer(profile).data,
#                 "curated_looks": LookSerializer(
#                     looks,
#                     many=True
#                 ).data,
#                 "for_you": RecommendationResultSerializer(
#                     recommendations,
#                     many=True
#                 ).data
#             },
#             status=status.HTTP_200_OK
#         )


# # 상세 Styling Look 조회 APIView
# class LookDetailAPIView(APIView):

#     def get(self, request, look_id):

#         look = get_object_or_404(
#             Look.objects.prefetch_related("items__product"),
#             id=look_id
#         )

#         serializer = LookDetailSerializer(look)

#         return Response(
#             {
#                 "success": True,
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )