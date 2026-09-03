from django.contrib import admin
from .models import ApprovalStage, Approval


@admin.register(ApprovalStage)
class ApprovalStageAdmin(admin.ModelAdmin):
    list_display = ["content_type", "order", "name", "approver_group", "approver_is_department_head", "min_amount"]
    list_filter = ["content_type", "approver_group"]
    ordering = ["content_type", "order"]

@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ["content_object", "stage", "status", "approved_by", "acted_at"]
    list_filter = ["status", "stage"]
    readonly_fields = ["content_type", "object_id", "stage", "created_by", "updated_by", "created_at", "updated_at"]
