from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Label, Status, Task

User = get_user_model()


class LabelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='pass123'
        )
        self.client.login(username='user', password='pass123')
        self.status = Status.objects.create(name='новый')

    def test_label_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:label_list'))
        self.assertEqual(response.status_code, 302)

    def test_label_list(self):
        response = self.client.get(reverse('tasks:label_list'))
        self.assertEqual(response.status_code, 200)

    def test_label_create(self):
        response = self.client.post(reverse('tasks:label_create'), {
            'name': 'bug'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='bug').exists())

    def test_label_update(self):
        label = Label.objects.create(name='old')
        response = self.client.post(
            reverse('tasks:label_update', args=[label.id]),
            {'name': 'updated'}
        )
        self.assertEqual(response.status_code, 302)
        label.refresh_from_db()
        self.assertEqual(label.name, 'updated')

    def test_label_delete(self):
        label = Label.objects.create(name='to-delete')
        response = self.client.post(
            reverse('tasks:label_delete', args=[label.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=label.id).exists())

    def test_label_delete_protected(self):
        label = Label.objects.create(name='protected')
        task = Task.objects.create(
            name='task1',
            status=self.status,
            author=self.user
        )
        task.labels.add(label)
        response = self.client.post(
            reverse('tasks:label_delete', args=[label.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(id=label.id).exists())

    def test_label_unique_name(self):
        Label.objects.create(name='duplicate')
        response = self.client.post(reverse('tasks:label_create'), {
            'name': 'duplicate'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')
