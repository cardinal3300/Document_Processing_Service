from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserRegisterSerializer, UserSerializer


User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Контроллер регистрации пользователей (доступна без авторизации)."""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(ModelViewSet):
    """Контроллер CRUD пользователей (только авторизованные)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
