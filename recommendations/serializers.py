from rest_framework import serializers

from .models import *


class VisitSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitSession
        fields = [
            "id",
            "session_key",
            "started_at",
            "ended_at",
        ]


class VisitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitHistory
        fields = [
            "id",
            "visit_session",
            "product",
            "sequence",
            "visited_at",
        ]


class StyleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleProfile
        fields = [
            "id",
            "visit_session",
            "summary",
            "tags",
            "analysis_mode",
            "created_at",
        ]

class StylingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StylingItem
        fields = [
            "id",
            "product",
            "order",
            "type",
        ]


class StylingResultSerializer(serializers.ModelSerializer):
    items = StylingItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = StylingResult
        fields = [
            "id",
            "style_profile",
            "look_order",
            "title",
            "subtitle",
            "description",
            "reason",
            "items",
        ]

class RecommendationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationResult
        fields = [
            "id",
            "style_profile",
            "product",
            "type",
            "reason",
            "score",
            "created_at",
        ]

class SavedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedProduct
        fields = [
            "id",
            "visit_session",
            "product",
            "created_at",
        ]

# 3.3 상세 Styling Look 조회용
class StylingProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source="category.name",
        read_only=True
    )

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "category",
            "image",
        ]

    def get_image(self, obj):
        product_image = obj.images.first()

        if product_image:
            return product_image.image.url

        return None


class StylingItemDetailSerializer(serializers.ModelSerializer):
    product = StylingProductSerializer(
        read_only=True
    )

    class Meta:
        model = StylingItem
        fields = [
            "id",
            "product",
            "order",
            "type",
        ]


class StylingResultDetailSerializer(serializers.ModelSerializer):
    items = StylingItemDetailSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = StylingResult
        fields = [
            "id",
            "style_profile",
            "look_order",
            "title",
            "subtitle",     # (선택 사항인 듯 - Look 밑에, 'aa 백 + bbb' 부분)
            "description",  # 스타일 설명
            "reason",       # 추천 이유
            "items",
        ]