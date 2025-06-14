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

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
