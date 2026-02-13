import uuid

from django.conf import settings
from django.db import models


class Document(models.Model):
    """Модель документа."""
    STATUS_CHOICES = (
        ('Pending', 'В ожидании'),
        ('Processing', 'В процессе'),
        ('Completed', 'Завершено'),
        ('Error', 'Ошибка'),
    )
    TARGET_FORMAT_CHOICES = (
        ('PDF', 'pdf'),
        ('CSV', 'csv'),
        ('XLSX', 'xlsx'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True
    )

    original_name = models.CharField(max_length=255)

    files = models.FileField(upload_to='uploads/%Y/%m/%d/')
    internal_file = models.FileField(upload_to='uploads/internal/', null=True, blank=True)
    converted_file = models.FileField(upload_to='uploads/converted/', null=True, blank=True)
    result_file = models.FileField(upload_to='results/%Y/%m/%d/', null=True, blank=True)

    mime_type = models.CharField(max_length=100, blank=True)
    size = models.PositiveBigIntegerField(help_text='Размер в байтах')

    parsed_data = models.JSONField(null=True, blank=True)

    target_format = models.CharField(
        max_length=10,
        choices=TARGET_FORMAT_CHOICES,
        default='PDF',
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    error_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.original_name} ({self.status})'

    class Meta:
        verbose_name = 'документ'
        verbose_name_plural = 'документы'
        ordering = ('-created_at',)
