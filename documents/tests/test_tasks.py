from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model

from documents.models import Document
from documents.tasks import (notify_admin_new_documents,
                             notify_user_document_status)

User = get_user_model()


@pytest.mark.django_db
@patch('documents.tasks.send_mail')
def test_notify_admin_new_documents(mock_send_mail, settings):
    """Проверяем, что при вызове задачи
        отправляется email администратору."""
    settings.DEFAULT_FROM_EMAIL = "no-reply@test.com"
    settings.ADMIN_EMAIL = "admin@test.com"

    user = User.objects.create_user(
        email='user@test.com',
        password='password'
    )

    doc = Document.objects.create(
        owner=user,
        batch_id='11111111-1111-1111-1111-111111111111',
        files='documents/test.txt',
        size=123,
        original_name='test.txt'
    )

    notify_admin_new_documents([str(doc.id)])

    mock_send_mail.assert_called_once()

    _, kwargs = mock_send_mail.call_args

    assert 'Новые документы' in kwargs['subject']
    assert kwargs["recipient_list"] == ['admin@test.com']


@pytest.mark.django_db
@patch('documents.tasks.send_mail')
def test_notify_user_status_change(mock_send_mail, settings):
    """Проверяем, что пользователю отправляется email
        при изменении статуса документа."""
    settings.DEFAULT_FROM_EMAIL = 'no-reply@test.com'

    user = User.objects.create_user(
        email='user2@test.com',
        password='password'
    )

    doc = Document.objects.create(
        owner=user,
        batch_id='22222222-2222-2222-2222-222222222222',
        files='documents/test2.txt',
        original_name='test2.txt',
        size=123,
        status='Approved'
    )

    notify_user_document_status(str(doc.id))

    mock_send_mail.assert_called_once()

    _, kwargs = mock_send_mail.call_args

    assert user.email in kwargs['recipient_list']
    assert 'документа' in kwargs['subject']
