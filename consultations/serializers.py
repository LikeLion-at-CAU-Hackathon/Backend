from rest_framework import serializers
from .models import ConsultationRequest


class ConsultationRequestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = ConsultationRequest
        fields = [
            "id",
            "product",
            "product_name",
            "request_type",
            "message",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]