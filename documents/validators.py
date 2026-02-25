import magic
import pyclamd
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_TOTAL_SIZE = 45 * 1024 * 1024  # 45MB
MAX_FILES_USER = 5

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


def validate_mime_type(file):
    file.seek(0)
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)

    if mime not in ALLOWED_MIME_TYPES:
        raise ValidationError(f"Недопустимый MIME тип: {mime}")
    return mime


def validate_virus(file):
    try:
        cd = pyclamd.ClamdUnixSocket()
        file.seek(0)
        result = cd.scan_stream(file.read())
        file.seek(0)

        if result:
            raise ValidationError("Файл заражён вирусом.")
    except Exception:
        # если ClamAV недоступен — можно логировать
        raise ValidationError("Антивирус недоступен.")