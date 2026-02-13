from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from documents.tasks import process_document
from documents.serializers import MultipleDocumentUploadSerializer, DocumentDetailSerializer
from documents.models import Document


class MultipleDocumentUploadView(generics.GenericAPIView):
    serializer_class = MultipleDocumentUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        documents = serializer.save()
        batch_id = documents[0].batch_id

        return Response({
            'batch_id': str(batch_id),
            'documents_count': len(documents),
            'documents': [
                {
                    'id': str(doc.id),
                    'status': doc.status,
                    'created': doc.created_at,
                    'type': doc.mime_type,
                    'target_format': doc.target_format,
                }
                for doc in documents
            ]
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        document = serializer.save()
        process_document.delay(str(document.id))


class DocumentDetailView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        documents = Document.objects.filter(batch_id=pk)

        if not documents.exists():
            return Response({"detail": "Not found"}, status=404)

        return Response({
            "batch_id": pk,
            "documents": [
                {
                    'id': str(doc.id),
                    'status': doc.status,
                }
                for doc in documents
            ]
        })
