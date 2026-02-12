from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from documents.serializers import MultipleDocumentUploadSerializer


class MultipleDocumentUploadView(generics.GenericAPIView):
    serializer_class = MultipleDocumentUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        documents = serializer.save()

        response_data = {
            "documents": [
                {
                    "id": str(doc.id),
                    "status": doc.status
                }
                for doc in documents
            ]
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
