from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name', 'email', 'username', 'password' ]
        extra_kwargs = {'password': {'write_only': True}}
     
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)