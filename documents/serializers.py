import uuid

from django.db import transaction
from rest_framework import serializers

from documents.models import Document
from documents.tasks import notify_admin_new_documents
from documents.validators import (validate_max_files_user,
                                  validate_max_limits_user)


class MultipleDocumentUploadSerializer(serializers.Serializer):
    """Сериализатор для загрузки пачки документов (до 5 файлов).
        После создания документов:
        - каждому присваивается единый batch_id
        - статус устанавливается PENDING
        - администратору отправляется уведомление через очередь."""
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )

    def validate_files(self, file_list):
        """Проверка ограничения."""
        validate_max_files_user(file_list)  # Проверяем количество загружаемых файлов
        validate_max_limits_user(file_list)  # Считаем общий вес загружаемых файлов
        return file_list

    @transaction.atomic
    def create(self, validated_data):
        """Создаёт документы со статусом PENDING
            и отправляет уведомление администратору."""
        request = self.context['request']
        files = validated_data['files']
        batch_uuid = uuid.uuid4()

        documents = []
        for uploaded_file in files:
            document = Document.objects.create(
                owner=request.user,
                batch_id=batch_uuid,
                original_name=uploaded_file.name,
                files=uploaded_file,
                size=uploaded_file.size,
                status='Pending'
            )
            documents.append(document)

        # Уведомление администратора через Celery
        notify_admin_new_documents.delay([str(doc.id) for doc in documents])
        return documents


class DocumentDetailSerializer(serializers.ModelSerializer):
    """Детальный просмотр документа."""

    class Meta:
        model = Document
        fields = (
            'id',
            'batch_id',
            'original_name',
            'size',
            'status',
            'created_at',
        )
        read_only_fields = fields
