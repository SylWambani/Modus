from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('suppliers', views.SupplierViewSet)
router.register('purchase-order-list', views.ViewPurchaseOrderViewSet)
router.register('purchase-order-create', views.AddPurchaseOrderViewSet, basename="order-create")
router.register('purchase-order-item', views.PurchaseOrderItemViewSet)


urlpatterns = router.urls