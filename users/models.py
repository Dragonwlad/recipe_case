from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    """Класс пользователей c авторизацией через email."""
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username