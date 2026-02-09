from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
