from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('approvals', views.ApprovalViewSet, basename="approvals")

urlpatterns = router.urls