from rest_framework import serializers
from django.db import transaction
from .models import PurchaseOrder, PurchaseOrderItem, Requisition, RequisitionItem, Supplier
from approvals.serializers import ApprovalSerializer

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields = ['id', 'name', 'email', 'phone', 'address']



class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'purchase_order', 'item', 'quantity', 'price_per_unit', 'total_amount']

class ViewPurchaseOrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    items= PurchaseOrderItemSerializer(many=True,read_only=True)
    # total_price = serializers.SerializerMethodField()

    
    
    # def get_total_price(self, cart):
    #     return sum([item.quantity * item.price_per_unit for item in cart.items.all()])
    class Meta:
        model=PurchaseOrder
        fields = ['id', 'order_number', 'supplier', 'items', 'total_price', 'created_at']

class AddPurchaseOrderSerializer(serializers.ModelSerializer):
    #supplier = SupplierSerializer()
    class Meta:
        model=PurchaseOrder
        fields = ['id','order_number', 'supplier', 'created_at']

class RequisitionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=RequisitionItem
        fields=['id', 'description', 'quantity', 'estimated_unit_cost', "total_cost"]

class AddRequisitionSerializer(serializers.ModelSerializer):
    items=RequisitionItemSerializer(many=True)
    class Meta:
        model=Requisition
        fields=['id', 'department', 'justification','items']
        read_only_fields = ['id']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        with transaction.atomic():
            requisition = Requisition.objects.create(**validated_data)
            for item_data in items_data:
                RequisitionItem.objects.create(requisition=requisition, **item_data)
        return requisition

class ViewRequisitionSerializer(serializers.ModelSerializer):
    requested_by = serializers.StringRelatedField(source="created_by")
    items = RequisitionItemSerializer(many=True, read_only=True)
    grand_total_cost = serializers.ReadOnlyField()
    approval_trail = ApprovalSerializer(source="approvals", many=True, read_only=True)


    class Meta:
        model = Requisition
        fields = [
            "id", "department", "justification", "status",
            "requested_by", "rejection_reason", "created_at", "updated_at", "items", "grand_total_cost", "approval_trail"
        ]
        read_only_fields = fields     