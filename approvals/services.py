from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from .models import Approval, ApprovalWorkflow, ApprovalAction

#finds workflow for the model and starts approval process
def start_approval(instance, user):
    #detects what model
    content_type = ContentType.objects.get_for_model(instance)

    #gets the correct workflow
    workflow = ApprovalWorkflow.objects.get(content_type=content_type)

    #start from step 1
    first_step = workflow.steps.first()

    #creates live approval instance
    return Approval.objects.create(
        content_type=content_type,
        object_id=instance.id,
        workflow=workflow,
        current_step=first_step
    )


def approve_step(approval, user, comment=""):
    # Check if user is in the group allowed to approve this step
    if approval.current_step.group not in user.groups.all():
        raise PermissionDenied("You are not allowed to approve this step")

    # Log action/save history
    ApprovalAction.objects.create(
        approval=approval,
        step=approval.current_step,
        user=user,
        action="APPROVED",
        comment=comment
    )

    # Move to next step or mark as approved if this was the last step
    next_step = approval.workflow.steps.filter(
        step_order__gt=approval.current_step.step_order
    ).first()

    if next_step:
        approval.current_step = next_step
    else:
        approval.status = "APPROVED"

    approval.save()

    return approval


def reject_step(approval, user, comment=""):
    if approval.current_step.group not in user.groups.all():
        raise PermissionDenied("You are not allowed to reject this step")

    ApprovalAction.objects.create(
        approval=approval,
        step=approval.current_step,
        user=user,
        action="REJECTED",
        comment=comment
    )

    approval.status = "REJECTED"
    approval.save()

    return approval