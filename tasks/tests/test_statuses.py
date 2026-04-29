from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Status, Task

User = get_user_model()


class StatusTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='pass123'
        )
        self.client.login(username='user', password='pass123')

    def test_status_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:status_list'))
        self.assertEqual(response.status_code, 302)

    def test_status_list(self):
        response = self.client.get(reverse('tasks:status_list'))
        self.assertEqual(response.status_code, 200)

    def test_status_create(self):
        response = self.client.post(reverse('tasks:status_create'), {
            'name': 'new-status'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='new-status').exists())

    def test_status_update(self):
        status = Status.objects.create(name='old')
        response = self.client.post(
            reverse('tasks:status_update', args=[status.id]),
            {'name': 'updated'}
        )
        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, 'updated')

    def test_status_delete(self):
        status = Status.objects.create(name='to-delete')
        response = self.client.post(
            reverse('tasks:status_delete', args=[status.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=status.id).exists())

    def test_status_delete_protected(self):
        status = Status.objects.create(name='protected')
        Task.objects.create(
            name='task1',
            status=status,
            author=self.user
        )
        response = self.client.post(
            reverse('tasks:status_delete', args=[status.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(id=status.id).exists())

    def test_status_unique_name(self):
        Status.objects.create(name='duplicate')
        response = self.client.post(reverse('tasks:status_create'), {
            'name': 'duplicate'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')
