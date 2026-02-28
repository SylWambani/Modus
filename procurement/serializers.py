from rest_framework import serializers

from .models import PurchaseOrder, PurchaseOrderItem, Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields = ['id', 'name', 'email', 'phone', 'address']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields = ['id', 'order_number', 'supplier', 'status', 'created_at']

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'purchase_order', 'quantity', 'price_per_unit']