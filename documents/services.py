import os
import json
import csv
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook
from documents.validators import validate_mime_type
from documents.models import Document


def detect_mime(document: Document) -> str:
    """Повторная проверка MIME-типа на уровне Celery worker.
    Защита от подмены файла после загрузки."""
    with document.files.open("rb") as f:
        mime = validate_mime_type(f)
    return mime


def normalize_to_internal(document: Document) -> str:
    """Приводит документ к внутреннему стандарту JSON."""
    file_path = document.files.path
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext in ['.jpg', '.jpeg', '.png', '.docx']:
        return convert_to_pdf(document)

    if ext in ['.csv', '.xlsx']:
        return convert_to_csv(document)

    return file_path


def convert_to_pdf(document):
    """Конвертация документа в PDF. (Упрощённая версия)."""
    output_path = os.path.join(settings.MEDIA_ROOT, 'internal', f'{document.id}.pdf')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    elements = [Paragraph(f'Converted files: {document.original_name}', styles['Normal'])]
    doc.build(elements)

    return f'internal/{document.id}.pdf'


def convert_to_csv(document):
    """Приведение таблиц к CSV."""
    output_path = os.path.join(settings.MEDIA_ROOT, 'internal', f'{document.id}.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Demo', 'Data'])
        writer.writerow(['Example', '123'])

    return f'internal/{document.id}.csv'


def convert_to_target(document):
    """Конвертация внутреннего файла в формат, выбранный пользователем."""
    target = document.target_format

    if target == 'PDF':
        return convert_to_pdf(document)

    if target == 'CSV':
        return convert_to_csv(document)

    if target == 'XLSX':
        output_path = os.path.join(settings.MEDIA_ROOT, 'converted', f'{document.id}.xlsx')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        wb = Workbook()
        ws = wb.active
        ws.append(['Example', 'Value'])
        ws.append(['Test', 100])
        wb.save(output_path)

        return f'converted/{document.id}.xlsx'

    return None


def parse_document(document: Document) -> dict:
    """Извлекает структурированные данные из документа internal_file."""
    if not document.internal_file:
        return {'error': 'Internal file не найден!'}

    file_path = document.internal_file.path
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    parsed_result = {}

    if ext == '.csv':
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return {'rows': list(reader)}
    else:
        parsed_result['message'] = f'Парсинг для типа {ext} пока не реализован'
    return parsed_result


def export_result(document: Document) -> str:
    """Сохраняет parsed_data в JSON-файл.
    Возвращает относительный путь для result_file."""
    if not document.parsed_data:
        return None

    result_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(result_dir, exist_ok=True)

    result_filename = f'{document.id}.json'
    result_path = os.path.join(result_dir, result_filename)

    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(document.parsed_data, f, ensure_ascii=False, indent=4)
    return f'results/{result_filename}'
