from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Label, Status, Task

User = get_user_model()


class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='pass123'
        )
        self.other = User.objects.create_user(
            username='other',
            password='pass123'
        )
        self.status = Status.objects.create(name='новый')
        self.label = Label.objects.create(name='bug')
        self.client.login(username='user', password='pass123')

    def test_task_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 302)

    def test_task_list(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)

    def test_task_create(self):
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'task1',
            'description': 'desc',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label.id],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='task1').exists())
        task = Task.objects.get(name='task1')
        self.assertEqual(task.author, self.user)
        self.assertEqual(task.executor, self.user)
        self.assertIn(self.label, task.labels.all())

    def test_task_update(self):
        task = Task.objects.create(
            name='task1',
            status=self.status,
            author=self.user
        )
        response = self.client.post(
            reverse('tasks:task_update', args=[task.id]),
            {
                'name': 'updated',
                'description': 'new',
                'status': self.status.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, 'updated')

    def test_task_detail(self):
        task = Task.objects.create(
            name='task1',
            status=self.status,
            author=self.user
        )
        response = self.client.get(
            reverse('tasks:task_detail', args=[task.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'task1')

    def test_task_delete_by_author(self):
        task = Task.objects.create(
            name='task1',
            status=self.status,
            author=self.user
        )
        response = self.client.post(
            reverse('tasks:task_delete', args=[task.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_task_delete_not_author(self):
        task = Task.objects.create(
            name='task1',
            status=self.status,
            author=self.user
        )
        self.client.login(username='other', password='pass123')
        response = self.client.post(
            reverse('tasks:task_delete', args=[task.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_task_unique_name(self):
        Task.objects.create(
            name='task1',
            status=self.status,
            author=self.user
        )
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'task1',
            'status': self.status.id,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')
