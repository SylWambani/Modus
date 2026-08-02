from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions



# class CanViewSupplier(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method == "GET":
#             return request.user.has_perm("procurement.view_supplier")
#         elif request.method == "POST":
#             return request.user.has_perm("procurement.add_supplier")
#         elif request.method == "DELETE":
#             return request.user.has_perm("procurement.delete_supplier")
#         elif request.method == ["PATCH", "PUT"]:
#             return request.user.has_perm("procurement.change_supplier")

#         return False
    
# class CanViewPurchaseOrder(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method == "GET":
#             return request.user.has_perm("procurement.view_purchase_order")
#         elif request.method == "POST":
#             return request.user.has_perm("procurement.add_purchase_order")
#         elif request.method == "DELETE":
#             return request.user.has_perm("procurement.delete_purchase_order")
#         elif request.method == ["PATCH", "PUT"]:
#             return request.user.has_perm("procurement.change_purchase_order")

#         return False

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')