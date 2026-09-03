from django.contrib import admin
from .models import Requisition, RequisitionItem


class RequisitionItemInline(admin.TabularInline):
    model = RequisitionItem
    extra = 0


@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ["id", "department", "status", "requested_by", "created_at"]
    list_filter = ["status", "department"]
    readonly_fields = ["status", "approved_by", "approved_at", "requested_by", "created_by", "updated_by"]
    inlines = [RequisitionItemInline]