from rest_framework import serializers
from .models import *

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

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(
        many=True, 
        read_only=True
    )
    
    stocks = StockSerializer(
        many=True, 
        read_only=True
    )

    class Meta:
        model = ProductDetail
        fields = [
            "id",
            "size",
            "color",
            "price",
            "images",
            "stocks",
        ]
        
class ProductSerializer(serializers.ModelSerializer):
    details = ProductDetailSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "specs",
            "background",
            "details",
        ]
        
class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = [
            "id",
            "color",
            "size",
            "price",
        ]

class ProductCompareSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ProductDetail
        fields = [
            "id",
            "size",
            "color",
            "price",
            "stocks",
        ]        
     
     
   
class ProductBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "background",
        ]
     
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            "id",
            "name",
            "description",
            "image",
            "order",
            "careguide",
        ]
        
class CareGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            "id",
            "name",
            "careguide",
        ]

    
class AIDocentRequestSerializer(serializers.Serializer):
    question = serializers.CharField()

class AIDocentResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()