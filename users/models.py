from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        max_length=256,
        verbose_name='Email'
    )

    avatar = models.ImageField(
        upload_to='users/avatars',
        verbose_name='Аватар',
        blank=True,
        null=True,
        help_text='Загрузите свой аватар'
    )

    phone = models.CharField(
        blank=True,
        verbose_name='Номер телефона',
        null=True,
        help_text='Введите номер телефона'
    )

    country = models.CharField(
        verbose_name='Страна',
        default='Россия'
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
