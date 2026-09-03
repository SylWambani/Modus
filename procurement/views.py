from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
# from auth import permissions
from auth.permissions import CustomDjangoModelPermissions, IsAuditorReadOnly, RequisitionApprovePermission, RequisitionConvertPermission 
from .serializers import AddPurchaseOrderSerializer, AddRequisitionSerializer, PurchaseOrderItemSerializer, SupplierSerializer, ViewPurchaseOrderSerializer, ViewRequisitionSerializer
from audit.views import AuditModelViewSet
from .models import PurchaseOrder, PurchaseOrderItem, Requisition, Supplier


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


class AddRequisitionViewSet(AuditModelViewSet):
    queryset=Requisition.objects.all()
    serializer_class = AddRequisitionSerializer
    http_method_names=["post"]
    # permission_classes=[IsAuthenticated]

    def get_permissions(self):
        return [permissions.IsAuthenticated()]
            
    def perform_create(self, serializer):
        requisition=serializer.save(requested_by=self.request.user, created_by=self.request.user, updated_by=self.request.user)
        requisition.start_approval_chain()

class ViewRequisitionViewSet(AuditModelViewSet):
    serializer_class = ViewRequisitionSerializer
    http_method_names = ["get", "post"]  # list/retrieve + action endpoints

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("procurement.view_requisition") or user.groups.filter(name="auditor").exists():
            return Requisition.objects.all()
        return Requisition.objects.filter(created_by=user)

    def get_permissions(self):
        if self.action in ["approve", "reject"]:
            return [permissions.IsAuthenticated(), RequisitionApprovePermission()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        requisition = self.get_object()
        requisition.approve(user=request.user)
        return Response(self.get_serializer(requisition).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        requisition = self.get_object()
        requisition.reject(user=request.user, reason=request.data.get("reason", ""))
        return Response(self.get_serializer(requisition).data)  