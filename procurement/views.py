from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from .serializers import SupplierSerializer
from .models import Supplier


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
