from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.account_url = reverse('account')
        self.transactions_url = reverse('transactions')
        self.transactions_csv_url = reverse('transactions_csv')
        self.username = 'test_user'
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username=self.username,
            email='testuser@example.com',
            password=self.password,
        )

    def test_index_url(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/index.html')

    def test_login_url(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/login.html')

    def test_register_url(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/register.html')

    def test_logout_url(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_account_url(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.account_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/account.html')

    def test_transactions_url(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.transactions_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/transactions.html')

    def test_transactions_csv_url(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.transactions_csv_url)
        self.assertEqual(response.status_code, 200)
