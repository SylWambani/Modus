import uuid
#from uuid import uuid4
from django.utils import timezone
from django.db import models, IntegrityError
from django.db.models import F, Sum
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from decimal import Decimal
from audit.models import AuditModel
from approvals.models import Approval, ApprovalStage
from organization.models import Department

class Supplier(AuditModel):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, 
    #     on_delete = models.PROTECT, 
    #     editable=False,
    #     related_name="created_suppliers"
    # )
    # updated_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.PROTECT,
    #     editable=False,
    #     related_name="updated_suppliers"
    # )
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # history = HistoricalRecords(inherit=True)

    def __str__(self):
        return self.name
        # return f"{self.name} (Created by:{self.created_by})"

    # class Meta:
    #     permissions = [
    #         ('view_supplier', 'Can view supplier')
    #     ]

class PurchaseOrder(AuditModel):
    # STATUS_CHOICES = (
    #     ('PENDING', 'Pending'),
    #     ('APPROVED', 'Approved'),
    #     ('RECEIVED', 'Received'),
    #     ('NOT_RECEIVED', 'Not Received'),
    # )

    order_number = models.CharField(max_length=50, unique=True, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    #status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    #accounts_approval
    #manager_approval
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, 
    #     on_delete = models.PROTECT, 
    #     editable=False,
    #     related_name="created_purchaseorder"
    # )
    # updated_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.PROTECT,
    #     editable=False,
    #     related_name="updated_purchaseorder"
    # )
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # history = HistoricalRecords(inherit=True)

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


class PurchaseOrderItem(AuditModel):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    item = models.CharField(max_length=50, null=False, blank=False)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=2)

    @property
    def total_amount(self):
        return self.quantity * self.price_per_unit
    
class Requisition(AuditModel):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CONVERTED = "converted"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending Approval"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_CONVERTED, "Converted to PO"),
    ]

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="requisitions"
    )

    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="requisitions")
    justification = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    rejection_reason = models.TextField(null=True, blank=True)
    approvals = GenericRelation(Approval)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("approve_requisition", "Can approve requisition"),
            ("convert_requisition", "Can convert requisition to PO"),
        ]

    @property
    def grand_total_cost(self):
        total = sum(
            (item.total_cost for item in self.items.all() if item.total_cost is not None),
            start=Decimal("0.00"),
        )
        return total

    def __str__(self):
        return f"Requisition #{self.pk} - {self.department} ({self.status})"

    def start_approval_chain(self):
        content_type = ContentType.objects.get_for_model(Requisition)
        stages = ApprovalStage.objects.filter(content_type=content_type).order_by("order")
        for stage in stages:
            Approval.objects.create(
                content_type=content_type,
                object_id=self.pk,
                stage=stage,
                created_by=self.created_by,
                updated_by=self.created_by,
            )

    def mark_approved(self, user):
        if self.status != self.STATUS_PENDING:
            raise ValidationError("Only pending requisitions can be approved.")
        self.status = self.STATUS_APPROVED
        self.approved_by = user
        self.approved_at = timezone.now()
        self.updated_by = user
        self.save()
    
    def mark_rejected(self, user, reason=""):
        if self.status != self.STATUS_PENDING:
            raise ValidationError("Only pending requisitions can be rejected.")
        self.status = self.STATUS_REJECTED
        self.approved_by = user
        self.approved_at = timezone.now()
        self.rejection_reason = reason
        self.updated_by = user
        self.save()


    def mark_converted(self, user):
        if self.status != self.STATUS_APPROVED:
            raise ValidationError("Only approved requisitions can be converted to a PO.")
        self.status = self.STATUS_CONVERTED
        self.updated_by = user
        self.save()


class RequisitionItem(models.Model):
    requisition = models.ForeignKey(
        Requisition, on_delete=models.CASCADE, related_name="items"
    )
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    estimated_unit_cost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    @property
    def total_cost(self):
        if self.estimated_unit_cost is None:
            return None
        return self.quantity * self.estimated_unit_cost

    def __str__(self):
        return f"{self.description} (x{self.quantity})"   
