from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from .permissions import CanViewSupplier, FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .serializers import AddPurchaseOrderSerializer, PurchaseOrderItemSerializer, SupplierSerializer, ViewPurchaseOrderSerializer
from audit.views import AuditModelViewSet
from .models import PurchaseOrder, PurchaseOrderItem, Supplier


class SupplierViewSet(AuditModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, CanViewSupplier]

class PurchaseOrderItemViewSet(AuditModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer

class ViewPurchaseOrderViewSet(AuditModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = ViewPurchaseOrderSerializer

class AddPurchaseOrderViewSet(AuditModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = AddPurchaseOrderSerializer

