from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html

from documents.models import Document
from documents.tasks import notify_user_document_status


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Админ-интерфейс для модерации документов.
        Позволяет:
        - просматривать загруженный файл
        - подтверждать документы
        - отклонять документы
        - автоматически уведомлять пользователя."""
    list_display = ('id', 'owner', 'status', 'file_link', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('owner__username', 'id')
    readonly_fields = ('file_preview', 'created_at')

    # Кнопки быстрых действий (Actions)
    actions = ['approve_docs', 'reject_docs']


    # 🔹 Кликабельная ссылка в списке
    def file_link(self, obj):
        if obj.files:
            return format_html(
                '<a href="{}" target="_blank" style="font-weight: bold;">Открыть файл</a>',
                obj.files.url
            )
        return 'Нет файла'

    file_link.short_description = 'Ссылка на файл'


    # 🔹 Просмотр файла внутри карточки
    def file_preview(self, obj):
        if obj.files:
            return format_html(
                '<a href="{}" target="_blank" style="font-weight: bold;">📂Скачать документ</a>',
                obj.files.url
            )
        return 'Нет файла'

    file_preview.short_description = 'Документ'


    @admin.action(description='✅ Подтвердить выбранные документы')
    def approve_docs(self, request, queryset):
        for doc in queryset:
            doc.status = 'Approved'
            doc.save(update_fields=['status'])

            transaction.on_commit(
                lambda doc_id=doc.id: notify_user_document_status.delay(str(doc_id))
            )

        self.message_user(request, f'Подтверждено документов: {queryset.count()}')


    @admin.action(description='❌ Отклонить выбранные документы')
    def reject_docs(self, request, queryset):
        for doc in queryset:
            doc.status = 'Rejected'
            doc.save(update_fields=['status'])

            transaction.on_commit(
                lambda doc_id=doc.id: notify_user_document_status.delay(str(doc_id))
            )

        self.message_user(request, f'Отклонено документов: {queryset.count()}')
