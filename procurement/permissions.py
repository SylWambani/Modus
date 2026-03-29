from rest_framework import permissions


class CanViewSupplier(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.has_perm("procurement.view_supplier")
        elif request.method == "POST":
            return request.user.has_perm("procurement.add_supplier")
        elif request.method == "DELETE":
            return request.user.has_perm("procurement.delete_supplier")

        return False
# class IsProcurementManager(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated and
#             request.user.groups.filter(
#                 name__in=[ "Procurement Manager"]
#             ).exists()
#         )

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')