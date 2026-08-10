from rest_framework import serializers
from .models import (
    Product,
    ProductDetail,
    ProductImage,
    Stock,
    NFCTag,
)

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = [
            "material",
            "dimensions",
            "weight",
            "hardware",
            "strap",
            "storage",
            "care",
        ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "order",
        ]

class StockSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True
    )

    class Meta:
        model = Stock
        fields = [
            "branch_name",
            "quantity",
        ]

class ProductSerializer(serializers.ModelSerializer):
    detail = ProductDetailSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    stocks = StockSerializer(many=True, read_only=True)

    collection_name = serializers.CharField(
        source="collection.name",
        read_only=True
    )

    group_name = serializers.CharField(
        source="group.name",
        read_only=True
    )
    
    group_id = serializers.IntegerField(
    source="group.id",
    read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "color",
            "size",

            "collection_name",
            "group_name",

            "detail",
            "images",
            "stocks",
            
            "group_id",
        ]
        
class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "size",
            "name",
            "price",
        ]
        
class ProductCompareSerializer(serializers.ModelSerializer):
    detail = ProductDetailSerializer(read_only=True)
    stocks = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "size",
            "price",
            "color",
            "detail",
            "stocks",
        ]