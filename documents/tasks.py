from celery import shared_task
from documents.models import Document
from documents.services import (
    detect_mime,
    normalize_to_internal,
    parse_document,
    export_result, convert_to_target,
)


@shared_task(bind=True)
def process_document(self, document_id: str):
    """Полный pipeline обработки:
    1. MIME проверка
    2. Конвертация к внутреннему стандарту
    3. Парсинг
    4. Конвертация в выбранный формат
    5. Обновление статуса
    При ошибке:
    → статус error
    → сохраняется сообщение ошибки."""
    if not document_id:
        raise ValueError('document_id is required')

    document = Document.objects.get(id=document_id)
    document.status = 'Processing'
    document.save(update_fields=['status'])

    try:
        # --- 1. MIME проверка ---
        mime = detect_mime(document)
        document.mime_type = mime
        document.save(update_fields=['mime_type'])

        # --- 2. Внутренний стандарт ---
        internal_path = normalize_to_internal(document)
        document.internal_file.name = internal_path
        document.save(update_fields=['internal_file'])

        # --- 3. Парсинг ---
        parsed_data = parse_document(document)
        document.parsed_data = parsed_data
        document.save(update_fields=['parsed_data'])

        # --- 4. Конвертация в выбранный формат ---
        converted_path = convert_to_target(document)
        if converted_path:
            document.converted_file.name = converted_path

        # --- 5. Экспорт ---
        result_path = export_result(document)
        if result_path:
            document.result_file.name = result_path

        # --- 6. Завершение ---
        document.status = 'Completed'
        document.save(update_fields=['status', 'result_file'])

    except Exception as e:
        document.status = 'Error'
        document.error_message = str(e)
        document.save(update_fields=['status', 'error_message'])
        raise

    print(document.result_file.path)
