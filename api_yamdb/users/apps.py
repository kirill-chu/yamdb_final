"""Base Apps file for Users App."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Default config class for Users App."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
