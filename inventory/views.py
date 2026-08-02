from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from django.db.models import Sum, F, DecimalField
from django.db.models.aggregates import Count
from .serializers import CategorySerializer, ProductInfoListSerializer, ProductSerializer, ProductVariantSerializer, StockMovementSerializer, UnitMeasurementSerializer
from .models import Category, Product, ProductVariant, StockMovement, UnitsMeasurement
from auth.permissions import CustomDjangoModelPermissions 

 

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        products_count=Count('product')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'Category cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class UnitMeasurementViewSet(ModelViewSet):
    queryset = UnitsMeasurement.objects.all()
    serializer_class = UnitMeasurementSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ProductVariantViewSet(ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ProductInfoListViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductInfoListSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class StockMovementViewSet(ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
