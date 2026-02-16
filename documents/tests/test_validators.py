import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError

from documents.validators import validate_max_files_user, validate_max_limits_user


@pytest.mark.django_db
class TestValidators:

    # --- Тест количества файлов ---
    def test_validate_max_files_user_limit_exceeded(self):
        # Создаем список из 6 "пустышек"
        files = [SimpleUploadedFile(f"file{i}.txt", b"content") for i in range(6)]
        with pytest.raises(ValidationError) as excinfo:
            validate_max_files_user(files)
        assert "Можно загрузить не более 5 файлов" in str(excinfo.value)

    # --- Тесты размеров ---
    def test_validate_max_limits_user_single_file_too_big(self):
        # Файл размером 11MB
        big_file = SimpleUploadedFile("big.pdf", b"0" * (11 * 1024 * 1024))
        with pytest.raises(ValidationError) as excinfo:
            validate_max_limits_user([big_file])
        assert "превышает допустимый размер" in str(excinfo.value)

    def test_validate_max_limits_total_size_exceeded(self):
        # 5 файлов по 10MB = 50MB (превышает общий лимит 45MB)
        files = [
            SimpleUploadedFile(f"f{i}.pdf", b"0" * (10 * 1024 * 1024))
            for i in range(5)
        ]
        with pytest.raises(ValidationError) as excinfo:
            validate_max_limits_user(files)
        assert "Суммарный размер" in str(excinfo.value)
