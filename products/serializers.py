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

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(
        many=True, 
        read_only=True
    )
    
    stocks = StockSerializer(
        many=True, 
        read_only=True
    )

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
            "specs",

            "collection_name",
            "group_name",
            "group_id",

            "images",
            "stocks",
        ]
        
class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
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
        model = Product
        fields = [
            "id",
            "name",
            "size",
            "price",
            "color",
            "specs",
            "stocks",
        ]
        
     

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = [
            "sections",
        ]

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            "id",
            "name",
            "location",
            "description",
            "image",
            "order",
        ]

class CareGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGuide
        fields = [
            "contents",
        ]