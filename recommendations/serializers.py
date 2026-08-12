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