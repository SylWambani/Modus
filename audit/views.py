from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet


class AuditModelViewSet(ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)