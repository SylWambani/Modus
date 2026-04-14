from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from .permissions import CustomDjangoModelPermissions 
from .serializers import AddPurchaseOrderSerializer, PurchaseOrderItemSerializer, SupplierSerializer, ViewPurchaseOrderSerializer
from audit.views import AuditModelViewSet
from .models import PurchaseOrder, PurchaseOrderItem, Supplier


class SupplierViewSet(AuditModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

class PurchaseOrderItemViewSet(AuditModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ViewPurchaseOrderViewSet(AuditModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = ViewPurchaseOrderSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class AddPurchaseOrderViewSet(AuditModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = AddPurchaseOrderSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


