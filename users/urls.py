from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('register', views.RegisterViewSet, basename='registration')
router.register('register-with-invite', views.RegisterWithInviteView.as_view(), basename='register-with-invite')

urlpatterns = router.urls
