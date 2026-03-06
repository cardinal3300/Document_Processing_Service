import uuid

from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError

from documents.models import Document
from documents.validators import (validate_max_files_user,
                                  validate_max_limits_user,
                                  validate_file_type)


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

        # Проверяем каждый файл
        for file in file_list:
            try:
                mime = validate_file_type(file)
                # сохраняем MIME во временное свойство
                file.detected_mime = mime

            except DjangoValidationError as e:
                raise serializers.ValidationError(str(e))
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
                mime_type=getattr(uploaded_file, 'detected_mime', uploaded_file.content_type),
                status='Pending'
            )
            documents.append(document)
        return documents


class DocumentDetailSerializer(serializers.ModelSerializer):
    """Детальный просмотр документа."""

    class Meta:
        model = Document
        fields = '__all__'
