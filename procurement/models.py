import uuid
#from uuid import uuid4
from django.db import models, IntegrityError
from django.db.models import F, Sum


class Supplier(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    address = models.TextField(max_length=255)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('RECEIVED', 'Received'),
        ('NOT_RECEIVED', 'Not Received'),
    )

    order_number = models.CharField(max_length=50, unique=True, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    #accounts_approval
    #manager_approval
    created_at = models.DateTimeField(auto_now_add=True)
    #created_by = models.

    def save(self, *args, **kwargs):
        if not self.pk:
            saved = False
            while not saved:
                self.order_number = uuid.uuid4().hex[:8].upper()
                try:
                    super().save(*args, **kwargs)
                    saved= True
                except IntegrityError:
                    continue
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
    
    @property
    def total_price(self):
        return self.items.aggregate(total=Sum(F('quantity') * F('price_per_unit')))['total'] or 0


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    #variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=2)

    @property
    def total_amount(self):
        return self.quantity * self.price_per_unit
    
    
