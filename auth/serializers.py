# auth/serializers.py

from rest_framework import serializers

class MeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    modules = serializers.ListField(child=serializers.CharField())
    permissions = serializers.ListField(child=serializers.CharField())