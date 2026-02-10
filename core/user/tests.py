from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        email = 'test@example.com'
        password = 'password123'
        user = self.User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', password='password123')

    def test_create_superuser(self):
        email = 'admin@example.com'
        password = 'password123'
        user = self.User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_invalid_flags(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='admin@example.com', password='password123', is_staff=False
            )
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='admin@example.com', password='password123', is_superuser=False
            )

    def test_string_representation(self):
        email = 'test@example.com'
        user = self.User.objects.create_user(email=email, password='password123')
        self.assertEqual(str(user), f"Username: {email}")

    def test_full_name(self):
        user = self.User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.full_name, "John Doe")
