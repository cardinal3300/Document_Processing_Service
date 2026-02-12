from django.db import transaction
from rest_framework import serializers

from documents.models import Document
from documents.validators import (validate_max_files_user,
                                  validate_max_limits_user, validate_mime_type,
                                  validate_virus)


class MultipleDocumentUploadSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )

    def validate_files(self, file_list):
        # Проверяем количество загружаемых файлов
        validate_max_files_user(file_list)

        # Считаем общий вес загружаемых файлов
        validate_max_limits_user(file_list)

        # Проверка каждого файла
        errors = []
        for file in file_list:
            try:
                validate_virus(file)  # Проверка на вирусы
                file.detected_mime = validate_mime_type(file)  # сохраняем MIME во временное свойство
            except Exception as e:
                errors.append({
                    'files': file.name,
                    'error': str(e)
                })
        if errors:
            raise serializers.ValidationError(errors)
        return file_list

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        files = validated_data['files']

        documents = []
        for uploaded_file in files:
            document = Document.objects.create(
                owner=request.user,
                original_name=uploaded_file.name,
                files=uploaded_file,
                size=uploaded_file.size,
                mime_type=uploaded_file.content_type,
            )
            documents.append(document)
        return documents
