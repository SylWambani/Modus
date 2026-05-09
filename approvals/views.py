from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Approval
from .serializers import ApprovalSerializer
from .services import approve_step, reject_step


class ApprovalViewSet(ReadOnlyModelViewSet):
    serializer_class = ApprovalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Approval.objects.filter(
            current_step__group__in=self.request.user.groups.all(),
            status="PENDING"
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        approval = self.get_object()
        approve_step(approval, request.user)

        return Response({"status": "approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        approval = self.get_object()
        reject_step(approval, request.user)

        return Response({"status": "rejected"})
