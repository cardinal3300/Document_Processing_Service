from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from documents.models import Document
from documents.serializers import (DocumentDetailSerializer,
                                   MultipleDocumentUploadSerializer)
from documents.tasks import notify_admin_new_documents


class MultipleDocumentUploadView(generics.GenericAPIView):
    serializer_class = MultipleDocumentUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        """Создает документы со статусом PENDING
            и возвращает batch_id для последующей проверки."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        documents = serializer.save()
        batch_id = documents[0].batch_id

        doc_ids = [doc.id for doc in documents]
        notify_admin_new_documents.delay(doc_ids)

        return Response({
            'batch_id': str(batch_id),
            'documents_count': len(documents),
            'documents': [
                {
                    'id': str(doc.id),
                    'status': doc.status,
                    'name': doc.original_name,
                    'created': doc.created_at,
                }
                for doc in documents
            ]
        }, status=status.HTTP_201_CREATED)


class DocumentDetailView(generics.GenericAPIView):
    serializer_class = DocumentDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, batch_id):
        documents = Document.objects.filter(
            batch_id=batch_id,
            owner=request.user
        )

        if not documents.exists():
            return Response({'detail': 'Not found'}, status=404)

        return Response({
            'batch_id': str(batch_id),
            'documents': [
                {
                    'id': str(doc.id),
                    'status': doc.status,
                    'name': doc.original_name,
                    'created': doc.created_at,
                }
                for doc in documents
            ]
        })
