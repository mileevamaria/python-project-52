from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким именем уже существует',
        },
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует',
        },
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
