from django.urls import path

from documents.views import MultipleDocumentUploadView

urlpatterns = [
    path('upload/', MultipleDocumentUploadView.as_view(), name='document-upload'),
]
