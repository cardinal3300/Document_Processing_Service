from django.urls import path

from documents.views import MultipleDocumentUploadView, DocumentDetailView


app_name = 'documents'

urlpatterns = [
    path('upload/', MultipleDocumentUploadView.as_view(), name='upload'),
    path('upload/<uuid:batch_id>/', DocumentDetailView.as_view(), name='upload-detail'),
]
