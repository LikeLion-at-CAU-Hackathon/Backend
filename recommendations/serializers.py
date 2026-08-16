from rest_framework import serializers

from products.models import Product
from .models import (
    StyleChip,
    StyleProfile,
    Look,
    LookProduct,
    VisitHistory,
    VisitSession,
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
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_category = serializers.CharField(
        source="product.category",
        read_only=True
    )

    class Meta:
        model = VisitHistory
        fields = [
            "id",
            "visit_session",
            "product",
            "product_name",
            "product_category",
            "sequence",
            "visited_at",
        ]


class StyleChipSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleChip
        fields = [
            "code",
            "label",
        ]


class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
        ]


class LookProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(
        source="product.id",
        read_only=True
    )

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_category = serializers.CharField(
        source="product.category",
        read_only=True
    )

    class Meta:
        model = LookProduct
        fields = [
            "product_id",
            "product_name",
            "product_category",
            "item_type",
            "source",
        ]


class LookSerializer(serializers.ModelSerializer):
    # Look에는 StyleChip 하나만 존재
    style_chip = StyleChipSerializer(
        read_only=True
    )

    # LookProduct 자체를 직렬화
    products = LookProductSerializer(
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
            "style_chip",
            "products",
        ]


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

    detail_id = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = LookProduct
        fields = [
            "item_type",
            "source",
            "product_id",
            "name",
            "category",
            "detail_id",
            "price",
            "color",
            "size",
            "image",
        ]

    def get_detail(self, obj):
        return obj.product.details.first()

    def get_detail_id(self, obj):
        detail = self.get_detail(obj)
        return detail.id if detail else None

    def get_price(self, obj):
        detail = self.get_detail(obj)
        return detail.price if detail else None

    def get_color(self, obj):
        detail = self.get_detail(obj)
        return detail.color if detail else None

    def get_size(self, obj):
        detail = self.get_detail(obj)
        return detail.size if detail else None

    def get_image(self, obj):
        detail = self.get_detail(obj)

        if not detail:
            return None

        product_image = detail.images.first()

        if not product_image:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                product_image.image.url
            )

        return product_image.image.url

class LookDetailSerializer(serializers.ModelSerializer):
    
    style_chip = StyleChipSerializer(
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
            "style_chip",
            "products",
        ]


class StyleProfileSerializer(serializers.ModelSerializer):
    style_chips = StyleChipSerializer(
        many=True,
        read_only=True
    )

    # StyleProfile에 연결된 Look 3개
    looks = LookSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = StyleProfile
        fields = [
            "id",
            "summary",
            "style_chips",
            "looks",
            "created_at",
        ]