from django.urls import path

from documents.views import DocumentDetailView, MultipleDocumentUploadView

app_name = 'documents'

urlpatterns = [
    path('upload/', MultipleDocumentUploadView.as_view(), name='upload'),
    path('upload/<uuid:batch_id>/', DocumentDetailView.as_view(), name='upload-detail'),
]
