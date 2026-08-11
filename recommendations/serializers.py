from rest_framework import serializers

from .models import (
    VisitSession,
    VisitHistory,
    StyleProfile,
)


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