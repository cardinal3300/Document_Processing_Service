from rest_framework import serializers

from documents.models import Document


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'file')

    def validate_file(self, file):
        max_size = 50 * 1024 * 1024  # 50 MB

        if file.size > max_size:
            raise serializers.ValidationError('Файл превышает допустимый размер')

        return file

    def create(self, validated_data):
        request = self.context['request']
        uploaded_file = validated_data['file']

        document = Document.objects.create(
            owner=request.user,
            original_name=uploaded_file.name,
            file=uploaded_file,
            size=uploaded_file.size,
            mime_type=uploaded_file.content_type,
        )

        return document
