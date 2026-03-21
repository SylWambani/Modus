import uuid
import inflect
from django.db import models
from django.db.models import Sum, F, DecimalField
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from rapidfuzz import process, fuzz
from .utils.normalization import normalize_variant_text
from .utils.product_matching import prevent_typo

p = inflect.engine()

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
    canonical = models.CharField(max_length=255, unique=True, editable=False, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category', 'canonical'],
                name='unique_variant_per_product'
            )
        ]

    def clean(self):
        super().clean()
        if not self.name:
            return
        
        val=self.name.strip().lower()
        singular = p.singular_noun(val) or val
        self.canonical = singular

        # Get all existing product names(excluding the current instance if editing)
        existing_products=Product.objects.filter(
            category=self.category,
            ).exclude(pk=self.pk)

        names = [p.name.lower() for p in existing_products]

        if not names:
            return
        
        # Fuzzy matching
        if existing_products:
            # Find the closest match, extractOne returns(match_string, score, index)
            match = process.extractOne(singular, names, scorer=fuzz.WRatio)

            if match:
                closest_name, score, _ = match

                closest_singular = p.singular_noun(closest_name.lower()) or closest_name.lower()

                # Set a threshold(90 is a good starting point for typos)
                if score > 85 or singular==closest_singular:
                    raise ValidationError(
                        f"A similar product '{closest_name}' already exists in this category"
                        f"(Confidence:{score:.0f}%).Please use the existing record or correct the typo."
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
    type = models.TextField(blank=True)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    buying_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])

    reorder_level = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'unit_of_measure', 'color', 'size'],
                name='unique_variant_per_product',
            )
        ]

    def clean(self):
        super().clean()

        # Normalize fields
        self.color = normalize_variant_text(self.color)
        self.size = normalize_variant_text(self.size)
        self.type = normalize_variant_text(self.type)

        # Get existing values for this product
        existing = ProductVariant.objects.filter(
            product=self.product,
        ).exclude(pk=self.pk)

        existing_colors = [v.color for v in existing if v.color]
        existing_sizes = [v.size for v in existing if v.size]
        existing_types = [v.type for v in existing if v.type]

        # 1️⃣ Block duplicates after normalization
        if self.type and self.type in existing_types:
            raise ValidationError(
                f"The type '{self.type}' already exists for this product."
            )
        if self.color and self.color in existing_colors:
            raise ValidationError(
                f"The color '{self.color}' already exists for this product."
            )
        if self.size and self.size in existing_sizes:
            raise ValidationError(
                f"The size '{self.size}' already exists for this product."
            )

        # Check typos
        prevent_typo(self.type, existing_types)
        prevent_typo(self.color, existing_colors)
        prevent_typo(self.size, existing_sizes)

    def save(self, *args, **kwargs):

        if not self.pk:
            cat = self.product.category.name[:3].upper()
            name = self.product.name[:3].upper()
            self.short_code = uuid.uuid4().hex[:8].upper()
            self.sku = f"{cat}-{name}-{self.short_code}"

        self.full_clean()
        super().save(*args, **kwargs)

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

    @property
    def current_stock(self):
        total = self.movements.aggregate(total=Sum('quantity'))['total']
        return total or 0

    def save(self, *args, **kwargs):
        if self.movement_type == 'OUT':
            self.quantity = -abs(self.quantity)
        elif self.movement_type == 'IN':
            self.quantity = abs(self.quantity)

        super().save(*args, **kwargs)


   
