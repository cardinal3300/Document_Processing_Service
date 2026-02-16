from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from documents.models import Document


@shared_task
def notify_admin_new_documents(doc_ids: list[str]) -> None:
    """Отправляет email администратору о новых загруженных документах."""
    doc = Document.objects.filter(id__in=doc_ids)
    count = doc.count()

    file_list = '\n'.join([f'- {d.original_name} (ID: {d.id})' for d in doc])

    send_mail(
        subject=f'Новые документы: {count} шт. поступили на модерацию',
        message=f'Пользователь загрузил пакет документов.\n\n'
                f'Список файлов:\n{file_list}\n\n'
                f'Проверьте их в админ-панели.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
    )


@shared_task
def notify_user_document_status(doc_id):
    """Отправляет пользователю уведомление о результате модерации."""
    try:
        doc = Document.objects.select_related('owner').get(id=doc_id)

        print(f"DEBUG: Отправка письма для {doc.id} на почту {doc.owner.email}")

        send_mail(
            subject=f'Обновление статуса документа #{doc.id}',
            message=f'Здравствуйте! Статус вашего документа изменен на: {doc.get_status_display()}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[doc.owner.email],
            fail_silently=False,
        )
    except Document.DoesNotExist:
        print(f"DEBUG: Документ {doc_id} не найден")
    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
