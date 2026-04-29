from django.contrib.auth.models import User
from django.db import models


class Status(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name='Имя',
        error_messages={
            'unique': 'Статус с таким названием уже существует',
        }
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(
        'Имя',
        max_length=255,
        unique=True,
        error_messages={
            'unique': 'Задача с таким именем уже существует',
        }
    )
    description = models.TextField('Описание', blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_tasks',
        verbose_name='Автор'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name='Исполнитель'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name
