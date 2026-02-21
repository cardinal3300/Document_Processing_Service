from django.test import TestCase

from users.models import User


class TestUserModel(TestCase):
    raw_password = 'admin'

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='admin@example.ru', password=self.raw_password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(self.raw_password))
