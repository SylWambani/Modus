from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from .serializers import AddPurchaseOrderSerializer, PurchaseOrderItemSerializer, SupplierSerializer, ViewPurchaseOrderSerializer
from .models import PurchaseOrder, PurchaseOrderItem, Supplier


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class PurchaseOrderItemViewSet(ModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer

class ViewPurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = ViewPurchaseOrderSerializer

class AddPurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = AddPurchaseOrderSerializer
