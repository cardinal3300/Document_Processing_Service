import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Document(models.Model):
    """Модель загруженного пользователем документа.
    Пользователь загружает документ через API.
    Администратор подтверждает или отклоняет его через Django admin.
    После модерации пользователю отправляется email-уведомление."""
    STATUS_CHOICES = (
        ('Pending', 'На модерации'),
        ('Approved', 'Подтверждён'),
        ('Rejected', 'Отклонён'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID документа')
    batch_id = models.UUIDField(
        db_index=True,
        verbose_name='ID группы загрузки',
        help_text='Общий UUID для пачки файлов, загруженных одним запросом.')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Владелец')

    files = models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name='Файл')
    original_name = models.CharField(max_length=255, verbose_name='Оригинальное имя файла')
    size = models.PositiveBigIntegerField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, db_index=True, verbose_name='Статус')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.original_name} ({self.status})'

    class Meta:
        verbose_name = 'документ'
        verbose_name_plural = 'документы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['batch_id']),
            models.Index(fields=['status']),
        ]
