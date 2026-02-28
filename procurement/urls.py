from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('suppliers', views.SupplierViewSet)


urlpatterns = router.urls