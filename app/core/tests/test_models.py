from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email(self):
        """Test creating a new user with email"""
        email = 'diego@oxd.com'
        password = 'Password123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'diego@TradeSpecifix.com'
        user = get_user_model().objects.create_user(email, 'MyPassword123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test create user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'MyPassword123')

    def test_create_new_superusre(self):
        user = get_user_model().objects.create_superuser(
            'test@tradespecifix.com',
            'MyPassword123'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


#  docker-compose run app sh -c "python manage.py test"
