from django.db import transaction
from rest_framework import serializers
from .models import Category, Product, ProductVariant, UnitsMeasurement

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products_count']

class UnitMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitsMeasurement
        fields = ['id', 'name'] 

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'category'] 


class ProductVariantSerializer(serializers.ModelSerializer):
    unit_of_measure= UnitMeasurementSerializer()

    class Meta:
        model = ProductVariant
        fields = ['id','unit_of_measure', 'sku', 'color', 'size', 'buying_price', 'selling_price', 'reorder_level']


class ProductInfoListSerializer(serializers.ModelSerializer):
    category= CategorySerializer()
    variants =  ProductVariantSerializer(many=True)

    class Meta:
        model=Product
        fields =[ 'id', 'name', 'category', 'variants'] 


