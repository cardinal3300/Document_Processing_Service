from django.contrib.auth import get_user_model
from rest_framework import permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Регистрация(доступна без авторизации)."""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(ModelViewSet):
    """CRUD пользователей (только авторизованные)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
