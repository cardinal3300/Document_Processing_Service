from rest_framework import serializers
from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_TOTAL_SIZE = 45 * 1024 * 1024  # 45MB
MAX_FILES_USER = 5

ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx'}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # docx
    'image/jpeg',
    'image/png',
    'text/csv',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # xlsx
}


def validate_max_files_user(file_list):
    """Валидация количества файлов пользователя."""
    if len(file_list) > MAX_FILES_USER:
        raise serializers.ValidationError(
            f'Можно загрузить не более {MAX_FILES_USER} файлов за один запрос.'
        )


def validate_max_limits_user(file_list):
    """Валидация размеров файла и общего размера всех файлов в загружаемом списке пользователя."""
    total_size = 0

    for file in file_list:
        if file.size > MAX_FILE_SIZE:
            raise ValidationError(f'Файл {file.name} превышает допустимый размер! Максимальный размер 10 MB')
        total_size += file.size

    if total_size > MAX_TOTAL_SIZE:
        raise ValidationError('Суммарный размер всех файлов превышает допустимый размер! Максимальный размер 45 MB.')
    return file_list


def validate_file_type(file):
    # Проверка расширения
    ext = "." + file.name.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'Недопустимое расширение файла: {ext}')

    # Проверка content-type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise ValidationError(
            f'Недопустимый MIME тип: {file.content_type}'
        )
