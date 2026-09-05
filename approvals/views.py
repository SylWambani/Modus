from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Approval
from .serializers import ApprovalSerializer


class ApprovalViewSet(viewsets.ModelViewSet):
    serializer_class = ApprovalSerializer
    http_method_names = ["get", "post"]

    def get_permissions(self):
        return [permissions.IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Approvals cannot be created directly."},
            status=405,
        )

    def get_queryset(self):
        user = self.request.user
        group_based_ids = Approval.objects.filter(
            status="pending",
            stage__approver_group__in=user.groups.all(),
        ).values_list("id", flat=True)

        dynamic_candidates = Approval.objects.filter(
            status="pending",
            stage__approver_is_department_head=True,
        )
        dynamic_ids = [a.id for a in dynamic_candidates if a.is_authorized(user)]

        return Approval.objects.filter(id__in=list(group_based_ids) + dynamic_ids)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        approval = self.get_object()
        try:
            approval.approve(user=request.user, comment=request.data.get("comment", ""))
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)
        return Response(self.get_serializer(approval).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        approval = self.get_object()
        try:
            approval.reject(user=request.user, comment=request.data.get("comment", ""))
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)
        return Response(self.get_serializer(approval).data)