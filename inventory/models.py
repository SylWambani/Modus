import uuid
from django.db import models
from django.db.models import Sum, F, DecimalField
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class UnitsMeasurement(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=255, blank=False)
    # slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_variant_per_product'
            )
        ]

    def clean(self):
        if Product.objects.filter(
            name=self.name,
            category=self.category,
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                "You already created this product."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    unit_of_measure = models.ForeignKey(UnitsMeasurement, on_delete=models.PROTECT)

    sku = models.CharField(max_length=50, unique=True, editable=False)
    short_code = models.CharField(max_length=8, unique=True, editable=False)

    # Optional attributes
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    buying_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])

    reorder_level = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'unit_of_measure', 'color', 'size'],
                name='unique_variant_per_product'
            )
        ]

    def clean(self):
        if ProductVariant.objects.filter(
            product=self.product,
            color=self.color,
            size=self.size,
            unit_of_measure=self.unit_of_measure
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                "You already created an SKU for this product variant."
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.pk:
            cat = self.product.category.name[:3].upper()
            name = self.product.name[:3].upper()
            self.short_code = uuid.uuid4().hex[:8].upper()
            self.sku = f"{cat}-{name}-{self.short_code}"

        super().save(*args, **kwargs)

    @property
    def current_stock(self):
        total = self.movements.aggregate(total=Sum('quantity'))['total']
        return total or 0

    def __str__(self):
        return f"{self.product.name} - {self.sku}"
    
    
#INVENTORY LEDGER
class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJ', 'Adjustment'),
    )

    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.movement_type == 'OUT':
            self.quantity = -abs(self.quantity)
        elif self.movement_type == 'IN':
            self.quantity = abs(self.quantity)

        super().save(*args, **kwargs)


   
