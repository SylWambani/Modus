from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('unit-measurement', views.UnitMeasurementViewSet)
router.register('products', views.ProductViewSet, basename='products')
router.register('products-variants', views.ProductVariantViewSet)
router.register('products-info-list', views.ProductInfoListViewSet)

# product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# product_router.register('variants', views.ProductVariantViewSet, basename='product-variant')

urlpatterns = router.urls 