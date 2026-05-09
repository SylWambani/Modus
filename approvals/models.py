from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from audit.models import AuditModel

class ApprovalWorkflow(models.Model):
    #name of the workflow eg. LPO approval flow
    name = models.CharField(max_length=100)

    # Which document this workflow applies to
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ApprovalStep(models.Model):
    #Links step to its workflow
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE, related_name="steps")

    #defines the sequence(1->2->3) of the steps in the workflow
    step_order = models.PositiveIntegerField()

    #Name of the step eg. "Manager Approval", "Finance Approval"
    name = models.CharField(max_length=100)

    # Group allowed to approve this step
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ["step_order"]

    def __str__(self):
        return f"{self.workflow.name} - Step {self.step_order}"

class Approval(AuditModel):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    # The workflow this approval is following
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE)

    # The current step in the workflow
    current_step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)

    # Current status of the approval
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    # Timestamp for when the approval was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_object} - {self.status}"

class ApprovalAction(AuditModel):
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE, related_name="actions")

    step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    action = models.CharField(max_length=20)  # APPROVED / REJECTED

    comment = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)