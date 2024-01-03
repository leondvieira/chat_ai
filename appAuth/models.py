from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from appBase.models import Base
from appAuth.manager import UserManager


class User(AbstractBaseUser, Base):
    username = models.CharField(
        verbose_name='usuário',
        max_length=30,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        verbose_name="Primeiro Nome",
        max_length=30
    )
    last_name = models.CharField(
        verbose_name="Último Nome",
        max_length=30
    )
    email = models.CharField(
        verbose_name="Email",
        max_length=255
    )
    user_type = models.CharField(
        verbose_name="Tipo de Usuário",
        choices=[
            ('manager', 'Síndico'),
            ('resident', 'Morador'),
        ],
        default='resident',
        max_length=8
    )
    superuser = models.BooleanField(
        verbose_name="Admin",
        default=False
    )
    objects = UserManager()
    USERNAME_FIELD = 'username'
