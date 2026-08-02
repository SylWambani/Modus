from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from procurement.permissions import CustomDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission


class MeView(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        # 1. MODULES (from Django Groups)
        modules = [
            group.name.lower()
            for group in user.groups.all()
        ]

        # 2. PERMISSIONS (your CustomDjangoModelPermissions feeds this)
        permissions = list(user.get_all_permissions())

        return Response({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "modules": modules,
            "permissions": permissions
        })