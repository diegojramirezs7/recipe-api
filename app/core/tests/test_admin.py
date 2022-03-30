from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    # function that runs before every test
    def setUp(self):
        # setup test client
        # we use self so that vars are available in other functions
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            email='diego@tradespecifix.com',
            password='MyPassword123'
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='diego@oxd.com',
            password='MyPassword123',
            name='Test User'
        )

    # need to test this because our user model uses email instead of username, so we need to customize admin as well
    def test_users_are_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
