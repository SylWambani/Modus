from rest_framework import serializers
from .models import PurchaseOrder, PurchaseOrderItem, Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields = ['id', 'name', 'email', 'phone', 'address']



class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'purchase_order', 'quantity', 'price_per_unit', 'total_amount']

class ViewPurchaseOrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    items= PurchaseOrderItemSerializer(many=True,read_only=True)
    # total_price = serializers.SerializerMethodField()

    
    
    # def get_total_price(self, cart):
    #     return sum([item.quantity * item.price_per_unit for item in cart.items.all()])
    class Meta:
        model=PurchaseOrder
        fields = ['id', 'order_number', 'supplier', 'items', 'total_price', 'status', 'created_at']

class AddPurchaseOrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    class Meta:
        model=PurchaseOrder
        fields = ['id','order_number', 'supplier', 'status', 'created_at']