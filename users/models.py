from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер для работы с email вместо username."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя."""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Телефон'
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')

    # Для премиум статуса
    is_premium = models.BooleanField(default=False, verbose_name='Премиум статус')

    # Лимит на загрузку файлов в месяц
    monthly_limit = models.PositiveIntegerField(default=50, verbose_name='Месячный лимит документов')

    # Храним дату, когда нужно обнулить счетчик лимитов
    limit_reset_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # Индекс для быстрого поиска по emai
        indexes = [models.Index(fields=['email']),]
