from rest_framework import serializers

from products.models import Product
from .models import (
    StyleChip,
    StyleProfile,
    Look,
    LookProduct,
)


# class VisitSessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VisitSession
#         fields = [
#             "id",
#             "session_key",
#             "started_at",
#             "ended_at",
#         ]


# class VisitHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VisitHistory
#         fields = [
#             "id",
#             "visit_session",
#             "product",
#             "sequence",
#             "visited_at",
#         ]

class StyleChipSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleChip
        fields = ["code", "label"]


class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category"]


class LookProductSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer(read_only=True)

    class Meta:
        model = LookProduct
        fields = ["id", "product"]


class LookSerializer(serializers.ModelSerializer):
    style_chips = StyleChipSerializer(
        many=True,
        read_only=True
    )

    products = serializers.SerializerMethodField()

    class Meta:
        model = Look
        fields = [
            "id",
            "look_order",
            "title",
            "subtitle",
            "description",
            "reason",
            "style_chips",
            "products",
        ]

    def get_products(self, obj):
        look_products = (
            obj.look_products
            .select_related("product")
            .all()
        )

        return ProductSimpleSerializer(
            [item.product for item in look_products],
            many=True
        ).data


class LookProductDetailSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(
        source="product.id",
        read_only=True
    )
    name = serializers.CharField(
        source="product.name",
        read_only=True
    )
    category = serializers.CharField(
        source="product.category",
        read_only=True
    )

    class Meta:
        model = LookProduct
        fields = [
            "item_type",
            "product_id",
            "name",
            "category",
        ]


class LookDetailSerializer(serializers.ModelSerializer):
    style_chips = StyleChipSerializer(
        many=True,
        read_only=True
    )

    products = LookProductDetailSerializer(
        source="look_products",
        many=True,
        read_only=True
    )

    class Meta:
        model = Look
        fields = [
            "id",
            "look_order",
            "title",
            "subtitle",
            "description",
            "reason",
            "style_chips",
            "products",
        ]



class StyleProfileSerializer(serializers.ModelSerializer):
    style_chips = StyleChipSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = StyleProfile
        fields = [
            "id",
            "summary",
            "style_chips",
            "created_at",
        ]