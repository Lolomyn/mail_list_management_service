from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=256,
        verbose_name='Email'
    )

    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('can_view_users', 'Can view users'),
            ('can_block_users', 'Can block users')
        ]

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
