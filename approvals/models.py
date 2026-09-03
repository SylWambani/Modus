from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from audit.models import AuditModel

class ApprovalStage(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)          # "Department Head Approval"
    order = models.PositiveIntegerField()
    approver_group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True)
    approver_is_department_head = models.BooleanField(
        default=False,
        help_text="If checked, the approver for this stage is the head of the department "
                   "attached to the object being approved (ignores Approver Group).",
    )
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["content_type", "order"]
        unique_together = ["content_type", "order"]

    def clean(self):
        if not self.approver_is_department_head and not self.approver_group:
            raise ValidationError(
                "Set an Approver Group, or check 'Approver is department head' — one of the two is required."
            )
        if self.approver_is_department_head and self.approver_group:
            raise ValidationError(
                "Choose only one: Approver Group OR 'Approver is department head', not both."
            )

    def __str__(self):
        approver = "Department Head" if self.approver_is_department_head else self.approver_group
        return f"{self.content_type.model} - {self.order}. {self.name} ({approver})"




class Approval(AuditModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    stage = models.ForeignKey(ApprovalStage, on_delete=models.PROTECT)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="approvals",
    )
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending",
    )
    acted_at = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ["stage__order"]
        unique_together = ["content_type", "object_id", "stage"]

    def _siblings(self):
        return Approval.objects.filter(content_type=self.content_type, object_id=self.object_id)

    def is_actionable(self):
        """All earlier stages (lower order) must already be approved."""
        return not self._siblings().filter(stage__order__lt=self.stage.order).exclude(status="approved").exists()

    def resolve_expected_approver(self):
        """Returns the specific User who should approve this stage, if resolvable
        dynamically (department head). Returns None if not applicable or not resolvable."""
        if not self.stage.approver_is_department_head:
            return None
        obj = self.content_object
        department = getattr(obj, "department", None)
        return getattr(department, "head", None) if department else None

    def is_authorized(self, user):
        """The single source of truth for 'can this user act on this approval'."""
        if self.stage.approver_is_department_head:
            expected = self.resolve_expected_approver()
            return expected is not None and expected.pk == user.pk
        if self.stage.approver_group:
            return self.stage.approver_group in user.groups.all()
        return False


    def approve(self, user, comment=""):
        if self.status != "pending":
            raise ValidationError("This approval stage has already been actioned.")
        if not self.is_actionable():
            raise ValidationError("Earlier approval stages must be completed first.")

        self.status = "approved"
        self.approved_by = user
        self.acted_at = timezone.now()
        self.comment = comment
        self.updated_by = user
        self.save()

        if not self._siblings().exclude(status="approved").exists():
            obj = self.content_object
            if hasattr(obj, "mark_approved"):
                obj.mark_approved(user)

    def reject(self, user, comment=""):
        if self.status != "pending":
            raise ValidationError("This approval stage has already been actioned.")
        
        self.status = "rejected"
        self.approved_by = user
        self.acted_at = timezone.now()
        self.comment = comment
        self.updated_by = user
        self.save()

        self._siblings().filter(status="pending").update(
            status="rejected", comment="Auto-rejected: an earlier stage was rejected."
        )
        obj = self.content_object
        if hasattr(obj, "mark_rejected"):
            obj.mark_rejected(user, reason=comment)