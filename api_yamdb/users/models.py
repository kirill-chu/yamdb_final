"""Mosels for Users App."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """New User class."""

    class Roles(models.TextChoices):
        """Roles for useer model."""

        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=40,
        blank=True,
    )

    class Meta:
        """Users meta class."""

        ordering = ['username']

    @property
    def is_admin(self):
        """Retrieve admin state."""
        self.is_superuser
        return self.role == self.Roles.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Retrieve admoderator state."""
        return self.role == self.Roles.MODERATOR
