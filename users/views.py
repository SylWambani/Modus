from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer
from .models import UserInvite

User = get_user_model()

class RegisterViewSet(ModelViewSet):
    serializer_class = UserRegistrationSerializer
    queryset=User.objects.all()
    permission_classes = []

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterWithInviteView(APIView):

    def post(self, request):
        token = request.data.get("token")
        password = request.data.get("password")

        try:
            invite = UserInvite.objects.get(token=token)
        except UserInvite.DoesNotExist:
            return Response({"error": "Invalid token"}, status=400)

        if invite.is_used:
            return Response({"error": "Invite already used"}, status=400)

        if invite.is_expired():
            return Response({"error": "Invite expired"}, status=400)

        if User.objects.filter(email=invite.email).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create_user(
            email=invite.email,
            password=password,
        )

        user.role = invite.role  # if your User model supports this
        user.save()

        invite.is_used = True
        invite.save()

        return Response({"message": "Account created successfully"}, status=201)