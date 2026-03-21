from django.urls import path
from rest_framework_nested import routers
from .views import RegisterViewSet


router = routers.DefaultRouter()
router.register('register', RegisterViewSet, basename='registration')

urlpatterns = router.urls
