from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from documents.models import Document
from documents.serializers import DocumentUploadSerializer


class DocumentUploadView(generics.CreateAPIView):

    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        document = serializer.save()
