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
    branch_id = serializers.IntegerField(
        source="branch.id",
        read_only=True
    )
    
    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True
    )
    
    class Meta:
        model = Stock
        fields = [
            "branch_id",
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
    name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    stocks = StockSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ProductDetail
        fields = [
            "id",
            "name",
            "size",
            "color",
            "price",
            "stocks",
        ]        
        
class NearbyBranchSerializer(serializers.Serializer):
    branch_id = serializers.IntegerField()
    branch_name = serializers.CharField()
    distance = serializers.FloatField()
    is_open = serializers.BooleanField()
    has_stock = serializers.BooleanField()
     
     
   
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

    
class AIAssistantRequestSerializer(serializers.Serializer):
    question = serializers.CharField()

class AIAssistantResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()