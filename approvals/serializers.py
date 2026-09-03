# approvals/serializers.py
from rest_framework import serializers
from .models import Approval

class ApprovalSerializer(serializers.ModelSerializer):
    stage_name = serializers.CharField(source="stage.name", read_only=True)
    approved_by = serializers.StringRelatedField()

    class Meta:
        model = Approval
        fields = ["id", "stage", "stage_name", "status", "approved_by", "acted_at", "comment"]
        read_only_fields = fields