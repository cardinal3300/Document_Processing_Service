from django.urls import path

from documents.views import MultipleDocumentUploadView, DocumentDetailView

urlpatterns = [
    path('upload/', MultipleDocumentUploadView.as_view(), name='document-upload'),
    path('upload/<uuid:pk>/', DocumentDetailView.as_view(), name='document-detail'),
]
