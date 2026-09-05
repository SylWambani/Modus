# approvals/serializers.py
from rest_framework import serializers
from .models import Approval

class ApprovalSerializer(serializers.ModelSerializer):
    stage_name = serializers.CharField(source="stage.name", read_only=True)
    approved_by = serializers.StringRelatedField()
    object_type = serializers.CharField(source="content_type.model", read_only=True)
    object_summary = serializers.SerializerMethodField()

    class Meta:
        model = Approval
        fields = [
            "id", "stage", "stage_name", "status", "approved_by", "acted_at", "comment",
            "object_type", "object_id", "object_summary",
        ]
        read_only_fields = fields

    def get_object_summary(self, approval):
        obj = approval.content_object
        if obj is None:
            return None

        model_name = approval.content_type.model
        if model_name == "requisition":
            return {
                "department": str(obj.department),
                "justification": obj.justification,
                "requested_by": str(obj.requested_by),
                "items": [
                    {
                        "description": item.description,
                        "quantity": item.quantity,
                        "estimated_unit_cost": str(item.estimated_unit_cost),
                        "total_cost": str(item.total_cost),
                    }
                    for item in obj.items.all()
                ],
                "grand_total_cost": str(obj.grand_total_cost),
            }
        return {"summary": str(obj)}