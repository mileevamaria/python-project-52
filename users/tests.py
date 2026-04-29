from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='pass123'
        )
        self.client.login(username='user', password='pass123')

    def test_users_list(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_user_create(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        response = self.client.post(
            reverse('users:update', args=[self.user.id]),
            {
                'username': 'updated',
                'first_name': 'New',
                'last_name': 'Name',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated')

    def test_user_delete(self):
        response = self.client.post(
            reverse('users:delete', args=[self.user.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class AuthTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='pass123'
        )

    def test_login(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'user',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'user',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='user', password='pass123')
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
